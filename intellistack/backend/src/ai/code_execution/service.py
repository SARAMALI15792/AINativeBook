"""
Code Execution Service
Handles secure code execution in sandboxed environments
Sprint 4: Interactive Code Blocks
"""

from typing import Optional, Dict, Any, List
from enum import Enum
import asyncio
import structlog
from datetime import datetime

logger = structlog.get_logger()


class ExecutionStatus(str, Enum):
    """Code execution status"""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    SECURITY_VIOLATION = "security_violation"


class CodeExecutionService:
    """
    Handles code execution in sandboxed environments
    Supports: Pyodide (browser), Docker (server-side)
    """

    def __init__(self):
        self.default_timeout = 30  # seconds
        self.max_output_length = 10000  # characters
        self.default_memory_limit = 128  # MB

    async def execute_code(
        self,
        code: str,
        language: str,
        environment: str = "pyodide",
        timeout: int = None,
        allowed_imports: Optional[List[str]] = None,
        blocked_functions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Execute code in specified environment

        Args:
            code: Code to execute
            language: Programming language (python, bash, cpp)
            environment: Execution environment (pyodide, docker, wasm)
            timeout: Max execution time in seconds
            allowed_imports: Whitelist of allowed imports
            blocked_functions: Blacklist of dangerous functions

        Returns:
            Dict with output, error, execution_time, status
        """
        timeout = timeout or self.default_timeout

        try:
            # Validate code before execution
            validation_result = await self._validate_code(
                code=code,
                language=language,
                allowed_imports=allowed_imports,
                blocked_functions=blocked_functions,
            )

            if not validation_result["valid"]:
                return {
                    "output": "",
                    "error": validation_result["error"],
                    "execution_time": 0,
                    "status": ExecutionStatus.SECURITY_VIOLATION,
                }

            # Execute based on environment
            if environment == "pyodide":
                result = await self._execute_pyodide(code, timeout)
            elif environment == "docker":
                result = await self._execute_docker(code, language, timeout)
            else:
                return {
                    "output": "",
                    "error": f"Unsupported environment: {environment}",
                    "execution_time": 0,
                    "status": ExecutionStatus.ERROR,
                }

            # Truncate output if too long
            if len(result["output"]) > self.max_output_length:
                result["output"] = (
                    result["output"][: self.max_output_length]
                    + f"\n\n[Output truncated - exceeded {self.max_output_length} characters]"
                )

            logger.info(
                "code_executed",
                language=language,
                environment=environment,
                status=result["status"],
                execution_time=result["execution_time"],
            )

            return result

        except asyncio.TimeoutError:
            logger.warning("code_execution_timeout", timeout=timeout)
            return {
                "output": "",
                "error": f"Execution timed out after {timeout} seconds",
                "execution_time": timeout,
                "status": ExecutionStatus.TIMEOUT,
            }
        except Exception as e:
            logger.error("code_execution_error", error=str(e))
            return {
                "output": "",
                "error": str(e),
                "execution_time": 0,
                "status": ExecutionStatus.ERROR,
            }

    async def validate_code(
        self,
        code: str,
        language: str,
        allowed_imports: Optional[List[str]] = None,
        blocked_functions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Validate code without execution
        Checks for syntax errors and security violations

        Returns:
            Dict with valid (bool), error (str), warnings (list)
        """
        return await self._validate_code(
            code=code,
            language=language,
            allowed_imports=allowed_imports,
            blocked_functions=blocked_functions,
        )

    async def _validate_code(
        self,
        code: str,
        language: str,
        allowed_imports: Optional[List[str]] = None,
        blocked_functions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Internal validation logic
        """
        warnings = []

        # Check for blocked functions
        if blocked_functions:
            for func in blocked_functions:
                if func in code:
                    return {
                        "valid": False,
                        "error": f"Blocked function detected: {func}",
                        "warnings": warnings,
                    }

        # Check for dangerous patterns
        dangerous_patterns = [
            "import os",
            "import sys",
            "import subprocess",
            "__import__",
            "eval(",
            "exec(",
            "compile(",
            "open(",  # File operations
            "file(",
        ]

        for pattern in dangerous_patterns:
            if pattern in code:
                # Check if it's in allowed imports
                if allowed_imports and any(
                    pattern.startswith(f"import {imp}") for imp in allowed_imports
                ):
                    continue

                return {
                    "valid": False,
                    "error": f"Security violation: {pattern} is not allowed",
                    "warnings": warnings,
                }

        # Language-specific validation
        if language == "python":
            try:
                compile(code, "<string>", "exec")
            except SyntaxError as e:
                return {
                    "valid": False,
                    "error": f"Syntax error: {str(e)}",
                    "warnings": warnings,
                }

        return {
            "valid": True,
            "error": None,
            "warnings": warnings,
        }

    async def _execute_pyodide(
        self,
        code: str,
        timeout: int,
    ) -> Dict[str, Any]:
        """
        Execute Python code in Pyodide (browser-based)
        Note: Actual Pyodide execution happens in frontend
        This is a placeholder for server-side validation
        """
        # In production, this would communicate with a Pyodide worker
        # For now, return a mock response
        return {
            "output": "# Pyodide execution happens in browser\n# This is a server-side placeholder",
            "error": None,
            "execution_time": 0.0,
            "status": ExecutionStatus.SUCCESS,
        }

    async def _execute_docker(
        self,
        code: str,
        language: str,
        timeout: int,
    ) -> Dict[str, Any]:
        """
        Execute code in Docker container
        Provides full environment with resource limits
        """
        start_time = datetime.now()

        try:
            # Build Docker command based on language
            if language == "python":
                docker_cmd = [
                    "docker",
                    "run",
                    "--rm",
                    "--network=none",  # No network access
                    f"--memory={self.default_memory_limit}m",
                    "--cpus=0.5",
                    f"--timeout={timeout}",
                    "python:3.11-slim",
                    "python",
                    "-c",
                    code,
                ]
            elif language == "bash":
                docker_cmd = [
                    "docker",
                    "run",
                    "--rm",
                    "--network=none",
                    f"--memory={self.default_memory_limit}m",
                    "--cpus=0.5",
                    f"--timeout={timeout}",
                    "bash:latest",
                    "bash",
                    "-c",
                    code,
                ]
            else:
                return {
                    "output": "",
                    "error": f"Unsupported language for Docker: {language}",
                    "execution_time": 0,
                    "status": ExecutionStatus.ERROR,
                }

            # Execute with timeout
            process = await asyncio.create_subprocess_exec(
                *docker_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )

                execution_time = (datetime.now() - start_time).total_seconds()

                if process.returncode == 0:
                    return {
                        "output": stdout.decode("utf-8"),
                        "error": None,
                        "execution_time": execution_time,
                        "status": ExecutionStatus.SUCCESS,
                    }
                else:
                    return {
                        "output": stdout.decode("utf-8"),
                        "error": stderr.decode("utf-8"),
                        "execution_time": execution_time,
                        "status": ExecutionStatus.ERROR,
                    }

            except asyncio.TimeoutError:
                process.kill()
                raise

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "output": "",
                "error": str(e),
                "execution_time": execution_time,
                "status": ExecutionStatus.ERROR,
            }
