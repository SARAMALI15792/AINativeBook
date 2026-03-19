"""
Enhanced Code Execution Routes
Extended API endpoints for interactive code blocks with streaming support
Sprint 5: Interactive Code Blocks
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
import structlog
import asyncio
import json

from src.shared.database import get_session as get_db
from src.core.auth.dependencies import get_current_user
from src.core.auth.models import User
from src.core.content.enhanced_models import InteractiveCodeBlock
from src.ai.code_execution.service import CodeExecutionService, ExecutionStatus

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/code", tags=["Code Execution"])

# Initialize service
code_execution_service = CodeExecutionService()

# Rate limiting (in-memory, should use Redis in production)
execution_counts = {}  # {user_id: {timestamp: count}}


class ExecuteCodeRequest(BaseModel):
    """Request to execute code"""
    code: str = Field(..., description="Code to execute")
    language: str = Field(..., description="python/bash/cpp")
    environment: str = Field(default="pyodide", description="pyodide/docker/wasm")
    timeout: Optional[int] = Field(default=30, description="Timeout in seconds")
    code_block_id: Optional[str] = Field(None, description="Optional code block ID for tracking")


class ExecuteCodeResponse(BaseModel):
    """Response from code execution"""
    output: str
    error: Optional[str]
    execution_time: float
    status: str
    environment: str
    truncated: bool = False


class ValidateCodeRequest(BaseModel):
    """Request to validate code"""
    code: str
    language: str
    allowed_imports: Optional[List[str]] = None
    blocked_functions: Optional[List[str]] = None


class ValidateCodeResponse(BaseModel):
    """Response from code validation"""
    valid: bool
    error: Optional[str]
    warnings: List[str]


class ExecutionEnvironmentInfo(BaseModel):
    """Information about execution environment"""
    name: str
    description: str
    supported_languages: List[str]
    features: List[str]
    limitations: List[str]
    resource_limits: dict


def check_rate_limit(user_id: str, limit: int = 10) -> bool:
    """
    Check if user has exceeded rate limit
    Returns True if within limit, False if exceeded
    """
    import time
    current_time = time.time()

    # Clean old entries (older than 1 minute)
    if user_id in execution_counts:
        execution_counts[user_id] = {
            ts: count for ts, count in execution_counts[user_id].items()
            if current_time - ts < 60
        }

    # Count executions in last minute
    total = sum(execution_counts.get(user_id, {}).values())

    if total >= limit:
        return False

    # Increment count
    if user_id not in execution_counts:
        execution_counts[user_id] = {}
    execution_counts[user_id][current_time] = execution_counts[user_id].get(current_time, 0) + 1

    return True


@router.post("/execute", response_model=ExecuteCodeResponse)
async def execute_code(
    request: ExecuteCodeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Execute code in sandboxed environment
    Supports Pyodide (browser) and Docker (server) execution
    """
    # Check rate limit
    if not check_rate_limit(str(current_user.id)):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Maximum 10 executions per minute.",
        )

    try:
        # Execute code
        result = await code_execution_service.execute_code(
            code=request.code,
            language=request.language,
            environment=request.environment,
            timeout=request.timeout,
        )

        # Track execution if code_block_id provided
        if request.code_block_id:
            # Update code block execution count
            code_block_result = await db.execute(
                select(InteractiveCodeBlock).where(
                    InteractiveCodeBlock.id == request.code_block_id
                )
            )
            code_block = code_block_result.scalar_one_or_none()

            if code_block:
                # Track in ContentEngagement (would need to link to content)
                pass

        logger.info(
            "code_executed",
            user_id=str(current_user.id),
            language=request.language,
            environment=request.environment,
            status=result["status"],
            execution_time=result["execution_time"],
        )

        return ExecuteCodeResponse(
            output=result["output"],
            error=result["error"],
            execution_time=result["execution_time"],
            status=result["status"],
            environment=request.environment,
            truncated=len(result["output"]) >= 10000,
        )

    except Exception as e:
        logger.error("code_execution_error", error=str(e), user_id=str(current_user.id))
        raise HTTPException(status_code=500, detail="Code execution failed")


@router.post("/execute/stream")
async def execute_code_stream(
    request: ExecuteCodeRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Execute code with streaming output
    Returns Server-Sent Events (SSE) for real-time output
    """
    # Check rate limit
    if not check_rate_limit(str(current_user.id)):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Maximum 10 executions per minute.",
        )

    async def generate_output():
        """Generate SSE events for code execution"""
        try:
            # Send start event
            yield f"data: {json.dumps({'type': 'start', 'timestamp': str(asyncio.get_event_loop().time())})}\n\n"

            # Execute code (in production, this should stream output in real-time)
            result = await code_execution_service.execute_code(
                code=request.code,
                language=request.language,
                environment=request.environment,
                timeout=request.timeout,
            )

            # Send output event
            if result["output"]:
                yield f"data: {json.dumps({'type': 'output', 'content': result['output']})}\n\n"

            # Send error event if any
            if result["error"]:
                yield f"data: {json.dumps({'type': 'error', 'content': result['error']})}\n\n"

            # Send completion event
            yield f"data: {json.dumps({'type': 'complete', 'status': result['status'], 'execution_time': result['execution_time']})}\n\n"

            logger.info(
                "code_executed_stream",
                user_id=str(current_user.id),
                language=request.language,
                status=result["status"],
            )

        except Exception as e:
            logger.error("stream_execution_error", error=str(e))
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(
        generate_output(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@router.post("/validate", response_model=ValidateCodeResponse)
async def validate_code(
    request: ValidateCodeRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Validate code without execution
    Checks syntax and security violations
    """
    try:
        result = await code_execution_service.validate_code(
            code=request.code,
            language=request.language,
            allowed_imports=request.allowed_imports,
            blocked_functions=request.blocked_functions,
        )

        logger.info(
            "code_validated",
            user_id=str(current_user.id),
            language=request.language,
            valid=result["valid"],
        )

        return ValidateCodeResponse(
            valid=result["valid"],
            error=result["error"],
            warnings=result["warnings"],
        )

    except Exception as e:
        logger.error("validation_error", error=str(e))
        raise HTTPException(status_code=500, detail="Code validation failed")


@router.get("/environments", response_model=List[ExecutionEnvironmentInfo])
async def get_execution_environments():
    """
    Get list of available execution environments
    Returns capabilities and limitations of each
    """
    environments = [
        ExecutionEnvironmentInfo(
            name="pyodide",
            description="Browser-based Python execution using WebAssembly",
            supported_languages=["python"],
            features=[
                "No server load",
                "Fast execution",
                "NumPy, Pandas, Matplotlib support",
                "Runs in browser",
                "No network access",
            ],
            limitations=[
                "Python only",
                "No ROS 2 support",
                "Limited to browser capabilities",
                "No file system access",
            ],
            resource_limits={
                "memory": "Browser dependent",
                "timeout": "30 seconds",
                "output_length": "10,000 characters",
            },
        ),
        ExecutionEnvironmentInfo(
            name="docker",
            description="Server-side execution in isolated Docker containers",
            supported_languages=["python", "bash", "cpp"],
            features=[
                "Full Python environment",
                "ROS 2 support",
                "Multiple languages",
                "File system access (isolated)",
                "Network isolation",
            ],
            limitations=[
                "Server load",
                "Slower startup",
                "Resource limits enforced",
                "Queue during high load",
            ],
            resource_limits={
                "memory": "128 MB",
                "cpu": "0.5 cores",
                "timeout": "30 seconds",
                "output_length": "10,000 characters",
            },
        ),
        ExecutionEnvironmentInfo(
            name="wasm",
            description="WebAssembly execution for compiled languages",
            supported_languages=["cpp", "rust"],
            features=[
                "Fast execution",
                "Browser-based",
                "No server load",
                "Compiled code performance",
            ],
            limitations=[
                "Compilation required",
                "Limited library support",
                "No ROS 2 support",
                "Experimental",
            ],
            resource_limits={
                "memory": "Browser dependent",
                "timeout": "30 seconds",
                "output_length": "10,000 characters",
            },
        ),
    ]

    return environments


@router.get("/stats")
async def get_execution_stats(
    current_user: User = Depends(get_current_user),
):
    """
    Get code execution statistics for current user
    Shows usage and limits
    """
    import time
    current_time = time.time()

    # Get user's recent executions
    user_executions = execution_counts.get(str(current_user.id), {})
    recent_count = sum(
        count for ts, count in user_executions.items()
        if current_time - ts < 60
    )

    return {
        "user_id": str(current_user.id),
        "executions_last_minute": recent_count,
        "rate_limit": 10,
        "remaining": max(0, 10 - recent_count),
        "reset_in_seconds": 60,
    }


@router.get("/code-blocks/{content_id}")
async def get_content_code_blocks(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all interactive code blocks for a content item
    Returns code blocks in order
    """
    try:
        result = await db.execute(
            select(InteractiveCodeBlock)
            .where(InteractiveCodeBlock.content_id == content_id)
            .order_by(InteractiveCodeBlock.order_index)
        )
        code_blocks = result.scalars().all()

        return {
            "content_id": content_id,
            "code_blocks": [
                {
                    "id": block.id,
                    "language": block.code_language,
                    "code": block.code_content,
                    "environment": block.execution_environment,
                    "is_editable": block.is_editable,
                    "is_executable": block.is_executable,
                    "title": block.title,
                    "description": block.description,
                    "expected_output": block.expected_output,
                    "order_index": block.order_index,
                }
                for block in code_blocks
            ],
        }

    except Exception as e:
        logger.error("get_code_blocks_error", error=str(e), content_id=content_id)
        raise HTTPException(status_code=500, detail="Failed to get code blocks")
