#!/usr/bin/env python3
"""
Planning Fixer Codebase Analysis Script

This script provides utilities for performing deep root cause analysis
and gap analysis of broken codebases as outlined in the planning-fixer-codebase skill.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any


class CodebaseAnalyzer:
    """
    A class to perform deep root cause analysis and gap analysis on codebases
    following the 5-phase framework of the planning-fixer-codebase skill.
    """

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.issues = []
        self.gaps = []
        self.dependencies = {}

    def phase_1_runtime_audit(self) -> Dict[str, Any]:
        """
        Phase 1: Perform runtime and functional audit.
        """
        results = {
            "runtime_errors": [],
            "logical_errors": [],
            "api_contract_failures": [],
            "auth_failures": [],
            "frontend_backend_misalignment": [],
            "env_inconsistencies": [],
            "production_failures": [],
            "build_deployment_issues": [],
            "database_inconsistencies": []
        }

        # Analyze runtime errors
        results["runtime_errors"] = self._find_runtime_errors()

        # Analyze logical errors
        results["logical_errors"] = self._find_logical_errors()

        # Check for broken API contracts
        results["api_contract_failures"] = self._find_api_contract_failures()

        # Check for authentication failures
        results["auth_failures"] = self._find_auth_failures()

        # Check for frontend-backend misalignment
        results["frontend_backend_misalignment"] = self._find_frontend_backend_misalignment()

        return results

    def _find_runtime_errors(self) -> List[Dict[str, Any]]:
        """Find runtime errors in the codebase."""
        errors = []

        # Look for common runtime error patterns
        for file_path in self._get_all_files():
            if file_path.suffix in ['.py', '.js', '.ts', '.tsx', '.jsx']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()
                        lines = content.split('\n')

                        for line_num, line in enumerate(lines, 1):
                            if 'undefined' in line and 'is not defined' in line:
                                errors.append({
                                    "file": str(file_path),
                                    "line": line_num,
                                    "code": line.strip(),
                                    "issue": "Runtime error - undefined variable",
                                    "severity": "Critical"
                                })
                            elif 'null' in line and 'pointer' in line.lower():
                                errors.append({
                                    "file": str(file_path),
                                    "line": line_num,
                                    "code": line.strip(),
                                    "issue": "Runtime error - null pointer",
                                    "severity": "Critical"
                                })
                    except Exception:
                        continue  # Skip files that can't be read

        return errors

    def _find_logical_errors(self) -> List[Dict[str, Any]]:
        """Find logical errors in the codebase."""
        errors = []

        for file_path in self._get_all_files():
            if file_path.suffix in ['.py', '.js', '.ts', '.tsx', '.jsx']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()
                        lines = content.split('\n')

                        for line_num, line in enumerate(lines, 1):
                            # Look for common logical error patterns
                            if 'if True:' in line and 'pass' in line:
                                errors.append({
                                    "file": str(file_path),
                                    "line": line_num,
                                    "code": line.strip(),
                                    "issue": "Logical error - unimplemented condition",
                                    "severity": "Major"
                                })
                            elif '= 0' in line and 'if' in line and ': 0' not in line:
                                # Potentially bad conditional logic
                                errors.append({
                                    "file": str(file_path),
                                    "line": line_num,
                                    "code": line.strip(),
                                    "issue": "Potential logical error - suspicious conditional",
                                    "severity": "Minor"
                                })
                    except Exception:
                        continue

        return errors

    def _find_api_contract_failures(self) -> List[Dict[str, Any]]:
        """Find broken API contracts."""
        failures = []

        # Look for API endpoints that don't match their documentation or usage
        for file_path in self._get_all_files():
            if 'api' in str(file_path).lower() or 'route' in str(file_path).lower():
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()
                        lines = content.split('\n')

                        for line_num, line in enumerate(lines, 1):
                            if 'def ' in line or 'function ' in line:
                                # Check if function signature matches expected API contract
                                if 'request' in line and 'response' not in content[line_num:line_num+10]:
                                    failures.append({
                                        "file": str(file_path),
                                        "line": line_num,
                                        "code": line.strip(),
                                        "issue": "API contract failure - missing response handling",
                                        "severity": "Major"
                                    })
                    except Exception:
                        continue

        return failures

    def _find_auth_failures(self) -> List[Dict[str, Any]]:
        """Find authentication flow failures."""
        failures = []

        for file_path in self._get_all_files():
            if 'auth' in str(file_path).lower() or 'login' in str(file_path).lower():
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()
                        lines = content.split('\n')

                        for line_num, line in enumerate(lines, 1):
                            if 'password' in line.lower() and 'hash' not in line.lower():
                                failures.append({
                                    "file": str(file_path),
                                    "line": line_num,
                                    "code": line.strip(),
                                    "issue": "Authentication failure - plain text password handling",
                                    "severity": "Critical"
                                })
                    except Exception:
                        continue

        return failures

    def _find_frontend_backend_misalignment(self) -> List[Dict[str, Any]]:
        """Find frontend-backend misalignments."""
        misalignments = []

        # Check for common misalignment patterns
        for file_path in self._get_all_files():
            if file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()
                        lines = content.split('\n')

                        for line_num, line in enumerate(lines, 1):
                            if 'fetch(' in line or 'axios' in line:
                                # Check for potential API endpoint mismatches
                                if 'localhost' in line and 'production' in content:
                                    misalignments.append({
                                        "file": str(file_path),
                                        "line": line_num,
                                        "code": line.strip(),
                                        "issue": "Frontend-backend misalignment - environment mismatch",
                                        "severity": "Major"
                                    })
                    except Exception:
                        continue

        return misalignments

    def phase_2_gap_analysis(self) -> Dict[str, Any]:
        """Phase 2: Perform comprehensive gap analysis."""
        gaps = {
            "architecture": [],
            "authentication_security": [],
            "error_handling": [],
            "logging_observability": [],
            "testing_coverage": [],
            "ci_cd_gaps": [],
            "code_quality": [],
            "performance_scalability": [],
            "configuration_risks": []
        }

        # Architecture analysis
        gaps["architecture"] = self._analyze_architecture_gaps()

        # Authentication and security analysis
        gaps["authentication_security"] = self._analyze_auth_security_gaps()

        # Error handling analysis
        gaps["error_handling"] = self._analyze_error_handling_gaps()

        # Logging and observability analysis
        gaps["logging_observability"] = self._analyze_logging_gaps()

        # Testing coverage analysis
        gaps["testing_coverage"] = self._analyze_testing_gaps()

        # CI/CD analysis
        gaps["ci_cd_gaps"] = self._analyze_ci_cd_gaps()

        # Code quality analysis
        gaps["code_quality"] = self._analyze_code_quality_gaps()

        # Performance and scalability analysis
        gaps["performance_scalability"] = self._analyze_performance_gaps()

        # Configuration risks analysis
        gaps["configuration_risks"] = self._analyze_configuration_gaps()

        return gaps

    def _analyze_architecture_gaps(self) -> List[Dict[str, Any]]:
        """Analyze architectural gaps."""
        gaps = []

        # Look for architecture-related issues
        for file_path in self._get_all_files():
            if file_path.suffix in ['.py', '.js', '.ts']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()

                        # Check for tight coupling, lack of separation of concerns
                        if 'import' in content:
                            imports = [line for line in content.split('\n') if 'import' in line]
                            if len(imports) > 20:  # Potentially too many dependencies
                                gaps.append({
                                    "file": str(file_path),
                                    "issue": "Architecture gap - tight coupling with many dependencies",
                                    "details": f"File imports {len(imports)} modules",
                                    "severity": "Major"
                                })
                    except Exception:
                        continue

        return gaps

    def _analyze_auth_security_gaps(self) -> List[Dict[str, Any]]:
        """Analyze authentication and security gaps."""
        gaps = []

        for file_path in self._get_all_files():
            if file_path.suffix in ['.py', '.js', '.ts']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()

                        if 'secret' in content.lower():
                            gaps.append({
                                "file": str(file_path),
                                "issue": "Security gap - potential hardcoded secret",
                                "details": "Found 'secret' in code",
                                "severity": "Critical"
                            })
                        if 'password' in content.lower() and 'env' not in content.lower():
                            gaps.append({
                                "file": str(file_path),
                                "issue": "Security gap - potential hardcoded password",
                                "details": "Found 'password' not linked to environment variable",
                                "severity": "Critical"
                            })
                    except Exception:
                        continue

        return gaps

    def _analyze_error_handling_gaps(self) -> List[Dict[str, Any]]:
        """Analyze error handling gaps."""
        gaps = []

        for file_path in self._get_all_files():
            if file_path.suffix in ['.py', '.js', '.ts']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()

                        # Look for try blocks without proper catch
                        if 'try:' in content or 'try {' in content:
                            if 'except' not in content and 'catch' not in content:
                                gaps.append({
                                    "file": str(file_path),
                                    "issue": "Error handling gap - try block without catch",
                                    "details": "Found try block without corresponding error handling",
                                    "severity": "Major"
                                })
                    except Exception:
                        continue

        return gaps

    def _analyze_logging_gaps(self) -> List[Dict[str, Any]]:
        """Analyze logging and observability gaps."""
        gaps = []

        for file_path in self._get_all_files():
            if file_path.suffix in ['.py', '.js', '.ts']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()

                        # Check if logging is present
                        if 'log' not in content.lower() and 'print' in content.lower():
                            gaps.append({
                                "file": str(file_path),
                                "issue": "Logging gap - using print instead of structured logging",
                                "details": "Found print statements but no structured logging",
                                "severity": "Minor"
                            })
                    except Exception:
                        continue

        return gaps

    def _analyze_testing_gaps(self) -> List[Dict[str, Any]]:
        """Analyze testing coverage gaps."""
        gaps = []

        test_files = [f for f in self._get_all_files() if 'test' in str(f).lower()]
        source_files = [f for f in self._get_all_files() if f.suffix in ['.py', '.js', '.ts'] and 'test' not in str(f)]

        if len(test_files) == 0:
            gaps.append({
                "issue": "Testing gap - no test files found",
                "details": "No tests detected in the codebase",
                "severity": "Major"
            })
        elif len(test_files) < len(source_files) * 0.3:  # Less than 30% test coverage
            gaps.append({
                "issue": "Testing gap - insufficient test coverage",
                "details": f"Found {len(test_files)} test files for {len(source_files)} source files",
                "severity": "Major"
            })

        return gaps

    def _analyze_ci_cd_gaps(self) -> List[Dict[str, Any]]:
        """Analyze CI/CD gaps."""
        gaps = []

        ci_files = [f for f in self._get_all_files() if any(name in str(f) for name in ['github', 'gitlab', 'circle', 'travis', '.github', 'jenkins'])]

        if not ci_files:
            gaps.append({
                "issue": "CI/CD gap - no CI/CD configuration found",
                "details": "No CI/CD configuration files detected",
                "severity": "Major"
            })

        return gaps

    def _analyze_code_quality_gaps(self) -> List[Dict[str, Any]]:
        """Analyze code quality gaps."""
        gaps = []

        for file_path in self._get_all_files():
            if file_path.suffix in ['.py', '.js', '.ts']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()
                        lines = content.split('\n')

                        # Check for very long functions (potential code smell)
                        if len(lines) > 200:
                            gaps.append({
                                "file": str(file_path),
                                "issue": "Code quality gap - very long file/function",
                                "details": f"File has {len(lines)} lines",
                                "severity": "Minor"
                            })
                    except Exception:
                        continue

        return gaps

    def _analyze_performance_gaps(self) -> List[Dict[str, Any]]:
        """Analyze performance and scalability gaps."""
        gaps = []

        for file_path in self._get_all_files():
            if file_path.suffix in ['.py', '.js', '.ts']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()

                        # Look for potential performance issues
                        if 'for ' in content and 'for ' in content and 'for ' in content:  # Nested loops
                            gaps.append({
                                "file": str(file_path),
                                "issue": "Performance gap - potential O(n^3) or worse algorithm",
                                "details": "Multiple nested loops detected",
                                "severity": "Major"
                            })
                    except Exception:
                        continue

        return gaps

    def _analyze_configuration_gaps(self) -> List[Dict[str, Any]]:
        """Analyze configuration and environment risks."""
        gaps = []

        for file_path in self._get_all_files():
            if 'config' in str(file_path).lower() or file_path.suffix == '.env':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()

                        if '.env' in str(file_path) and 'secret' in content.lower():
                            gaps.append({
                                "file": str(file_path),
                                "issue": "Configuration risk - secrets in environment file",
                                "details": "Potentially sensitive information in .env file",
                                "severity": "Critical"
                            })
                    except Exception:
                        continue

        return gaps

    def phase_3_dependency_mapping(self) -> Dict[str, Any]:
        """Phase 3: Create module dependency mapping."""
        dependencies = {}

        # Analyze file dependencies
        for file_path in self._get_all_files():
            if file_path.suffix in ['.py', '.js', '.ts']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()
                        imports = []

                        if file_path.suffix == '.py':
                            # Python imports
                            for line in content.split('\n'):
                                if line.strip().startswith('import ') or ' from ' in line:
                                    parts = line.split()
                                    if 'import' in parts:
                                        import_idx = parts.index('import')
                                        if import_idx > 0:
                                            imports.append(parts[import_idx - 1])

                        elif file_path.suffix in ['.js', '.ts']:
                            # JavaScript/TypeScript imports
                            for line in content.split('\n'):
                                if 'import ' in line:
                                    parts = line.replace('{', ' ').replace('}', ' ').replace('from', ' ').split()
                                    for part in parts:
                                        if part != 'import' and len(part) > 1:
                                            imports.append(part)

                        dependencies[str(file_path)] = imports
                    except Exception:
                        continue

        return dependencies

    def _get_all_files(self) -> List[Path]:
        """Get all files in the project path."""
        all_files = []
        for root, dirs, files in os.walk(self.project_path):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'dist', 'build']]

            for file in files:
                if not file.startswith('.') or file in ['.env', '.env.example']:
                    all_files.append(Path(root) / file)

        return all_files

    def run_full_analysis(self) -> Dict[str, Any]:
        """Run the complete 5-phase analysis."""
        print(f"Starting analysis of codebase: {self.project_path}")

        print("Phase 1: Running runtime and functional audit...")
        phase_1_results = self.phase_1_runtime_audit()

        print("Phase 2: Running comprehensive gap analysis...")
        phase_2_results = self.phase_2_gap_analysis()

        print("Phase 3: Creating dependency mapping...")
        phase_3_results = self.phase_3_dependency_mapping()

        full_results = {
            "phase_1_runtime_audit": phase_1_results,
            "phase_2_gap_analysis": phase_2_results,
            "phase_3_dependency_mapping": phase_3_results,
            "summary": self._generate_summary(phase_1_results, phase_2_results)
        }

        print("Analysis complete!")
        return full_results

    def _generate_summary(self, phase_1_results: Dict, phase_2_results: Dict) -> Dict[str, Any]:
        """Generate a summary of the analysis results."""
        critical_issues = 0
        major_issues = 0
        minor_issues = 0

        # Count issues from phase 1
        for category, issues in phase_1_results.items():
            for issue in issues:
                if issue.get('severity') == 'Critical':
                    critical_issues += 1
                elif issue.get('severity') == 'Major':
                    major_issues += 1
                elif issue.get('severity') == 'Minor':
                    minor_issues += 1

        # Count issues from phase 2
        for category, gaps in phase_2_results.items():
            for gap in gaps:
                if gap.get('severity') == 'Critical':
                    critical_issues += 1
                elif gap.get('severity') == 'Major':
                    major_issues += 1
                elif gap.get('severity') == 'Minor':
                    minor_issues += 1

        return {
            "total_critical_issues": critical_issues,
            "total_major_issues": major_issues,
            "total_minor_issues": minor_issues,
            "recommendation": "Prioritize critical and major issues before implementing fixes"
        }


def main():
    if len(sys.argv) != 2:
        print("Usage: python codebase_analyzer.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]

    if not os.path.exists(project_path):
        print(f"Error: Path {project_path} does not exist")
        sys.exit(1)

    analyzer = CodebaseAnalyzer(project_path)
    results = analyzer.run_full_analysis()

    # Print results in a formatted way
    print("\n" + "="*60)
    print("CODEBASE ANALYSIS RESULTS")
    print("="*60)

    print(f"\nSUMMARY:")
    print(f"Critical Issues: {results['summary']['total_critical_issues']}")
    print(f"Major Issues: {results['summary']['total_major_issues']}")
    print(f"Minor Issues: {results['summary']['total_minor_issues']}")
    print(f"\nRecommendation: {results['summary']['recommendation']}")

    print(f"\nDETAILED RESULTS:")
    print(f"\nPHASE 1 - Runtime Audit:")
    for category, issues in results['phase_1_runtime_audit'].items():
        if issues:
            print(f"  {category.replace('_', ' ').title()}: {len(issues)} issues found")
            for issue in issues[:3]:  # Show first 3 issues
                print(f"    - {issue['file']}:{issue['line']} - {issue['issue']}")
            if len(issues) > 3:
                print(f"    ... and {len(issues) - 3} more")

    print(f"\nPHASE 2 - Gap Analysis:")
    for category, gaps in results['phase_2_gap_analysis'].items():
        if gaps:
            print(f"  {category.replace('_', ' ').title()}: {len(gaps)} gaps found")
            for gap in gaps[:3]:  # Show first 3 gaps
                print(f"    - {gap.get('file', 'N/A')} - {gap['issue']}")
            if len(gaps) > 3:
                print(f"    ... and {len(gaps) - 3} more")


if __name__ == "__main__":
    main()
