#!/usr/bin/env python3
"""
Codebase Analysis Script

This script helps perform initial analysis of a codebase by identifying key file types,
structure, and common patterns that might indicate potential issues in a production environment.
"""

import os
import sys
from pathlib import Path
import json
import re
from typing import List, Dict, Any


class CodebaseAnalyser:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.findings = {
            "architecture": {},
            "auth_system": {},
            "file_connections": {},
            "deployment_config": {},
            "critical_issues": [],
            "major_issues": [],
            "minor_issues": []
        }

    def analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze the overall project structure"""
        structure = {
            "frontend": [],
            "backend": [],
            "config": [],
            "tests": [],
            "other": []
        }

        # Common patterns for different types of files
        frontend_patterns = [".js", ".jsx", ".ts", ".tsx", ".vue", ".html", ".css", ".scss"]
        backend_patterns = [".py", ".java", ".php", ".rb", ".go", ".rs"]
        config_patterns = [".env", ".json", ".yml", ".yaml", ".toml", ".xml"]

        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_path)

                if any(file.endswith(pattern) for pattern in frontend_patterns):
                    structure["frontend"].append(str(relative_path))
                elif any(file.endswith(pattern) for pattern in backend_patterns):
                    structure["backend"].append(str(relative_path))
                elif any(pattern in file for pattern in config_patterns):
                    structure["config"].append(str(relative_path))
                elif "test" in str(relative_path).lower() or "spec" in str(relative_path).lower():
                    structure["tests"].append(str(relative_path))
                else:
                    structure["other"].append(str(relative_path))

        return structure

    def analyze_auth_system(self) -> Dict[str, Any]:
        """Look for authentication-related files and patterns"""
        auth_patterns = [
            "auth",
            "login",
            "register",
            "session",
            "jwt",
            "token",
            "passport",
            "oauth"
        ]

        auth_files = []

        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                file_path = Path(root) / file
                if any(pattern in file.lower() for pattern in auth_patterns):
                    auth_files.append(str(file_path.relative_to(self.project_path)))

                    # Look inside the file for auth-specific patterns
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                            # Check for common auth-related patterns
                            if "jwt" in content.lower():
                                self.findings["auth_system"].setdefault("jwt_usage", []).append(str(file_path))
                            if "bcrypt" in content.lower() or "password" in content.lower():
                                self.findings["auth_system"].setdefault("password_handling", []).append(str(file_path))
                            if "session" in content.lower():
                                self.findings["auth_system"].setdefault("session_handling", []).append(str(file_path))
                            if re.search(r"login|signin|authenticate", content, re.IGNORECASE):
                                self.findings["auth_system"].setdefault("auth_endpoints", []).append(str(file_path))
                            if "cors" in content.lower():
                                self.findings["auth_system"].setdefault("cors_config", []).append(str(file_path))
                    except:
                        # Skip files that can't be read
                        pass

        return {"auth_files": auth_files}

    def find_api_endpoints(self) -> List[str]:
        """Find potential API endpoints"""
        endpoint_patterns = [
            r"get\s*\(",
            r"post\s*\(",
            r"put\s*\(",
            r"delete\s*\(",
            r"route\s*\(",
            r"app\.",
            r"router\."
        ]

        endpoints = []

        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(('.js', '.ts', '.py', '.java', '.php', '.rb')):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                            for pattern in endpoint_patterns:
                                if re.search(pattern, content, re.IGNORECASE):
                                    # Look for specific route definitions
                                    route_matches = re.findall(r'["\'](/[\w/-]*)["\']', content)
                                    for match in route_matches:
                                        if match not in endpoints:
                                            endpoints.append((str(file_path.relative_to(self.project_path)), match))
                    except:
                        pass

        return endpoints

    def check_environment_config(self) -> Dict[str, Any]:
        """Look for environment configuration files"""
        env_files = []
        config_vars = []

        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if ".env" in file or "config" in file.lower() or "setting" in file.lower():
                    file_path = Path(root) / file
                    env_files.append(str(file_path.relative_to(self.project_path)))

                    # Try to read environment variables
                    if file.endswith('.env') or 'config' in file.lower():
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                env_vars = re.findall(r'^\s*([A-Z_][A-Z0-9_]*)\s*=', content, re.MULTILINE)
                                config_vars.extend(env_vars)
                        except:
                            pass

        return {"env_files": env_files, "config_vars": config_vars}

    def check_import_exports(self) -> Dict[str, Any]:
        """Check for import/export patterns"""
        import_patterns = {
            "javascript": [r'import\s+.*\s+from', r'export\s+', r'require\s*\('],
            "python": [r'import\s+\w+', r'from\s+\w+\s+import'],
            "java": [r'import\s+\w+(\.\w+)*;'],
        }

        imports = {"javascript": [], "python": [], "java": []}

        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_path)

                # Check file type and look for import patterns
                if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for pattern in import_patterns["javascript"]:
                                matches = re.findall(pattern, content)
                                if matches:
                                    imports["javascript"].append({
                                        "file": str(relative_path),
                                        "pattern": pattern,
                                        "count": len(matches)
                                    })
                    except:
                        pass
                elif file.endswith('.py'):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for pattern in import_patterns["python"]:
                                matches = re.findall(pattern, content)
                                if matches:
                                    imports["python"].append({
                                        "file": str(relative_path),
                                        "pattern": pattern,
                                        "count": len(matches)
                                    })
                    except:
                        pass

        return imports

    def run_full_analysis(self) -> Dict[str, Any]:
        """Run the complete analysis"""
        print("Starting comprehensive codebase analysis...")

        # Phase 1: Architecture analysis
        print("Phase 1: Analyzing project structure...")
        self.findings["architecture"] = self.analyze_project_structure()

        # Phase 2: Authentication system analysis
        print("Phase 2: Analyzing authentication system...")
        self.findings["auth_system"].update(self.analyze_auth_system())

        # Phase 3: API endpoints and connections
        print("Phase 3: Finding API endpoints...")
        endpoints = self.find_api_endpoints()
        self.findings["file_connections"]["api_endpoints"] = endpoints

        # Phase 4: Environment configuration
        print("Phase 4: Checking environment configuration...")
        self.findings["deployment_config"] = self.check_environment_config()

        # Phase 5: Import/export analysis
        print("Phase 5: Checking import/export patterns...")
        self.findings["file_connections"]["imports"] = self.check_import_exports()

        # Identify potential issues based on analysis
        self.identify_issues()

        print("Analysis complete!")
        return self.findings

    def identify_issues(self):
        """Identify potential issues based on analysis"""
        # Check for missing environment files that might be needed in production
        env_files = self.findings["deployment_config"]["env_files"]
        if not any(".env" in f for f in env_files):
            self.findings["critical_issues"].append("No .env files found - potential issue with environment configuration in production")

        # Check for hardcoded secrets (basic check)
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(('.js', '.py', '.ts', '.java')):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if "secret" in content.lower() or "password" in content.lower():
                                # Check if it's hardcoded (not from environment)
                                if "=" in content and ("secret" in content.lower() or "password" in content.lower()):
                                    # This is a basic check - could be more sophisticated
                                    self.findings["major_issues"].append(f"Potential hardcoded secret detected in {file_path}")
                    except:
                        pass


def main():
    if len(sys.argv) < 2:
        print("Usage: python codebase_analysis.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]

    if not os.path.exists(project_path):
        print(f"Error: Path {project_path} does not exist")
        sys.exit(1)

    analyser = CodebaseAnalyser(project_path)
    findings = analyser.run_full_analysis()

    # Print summary
    print("\n" + "="*50)
    print("CODEBASE ANALYSIS SUMMARY")
    print("="*50)

    print(f"\n📁 Project Structure:")
    for category, files in findings["architecture"].items():
        print(f"  {category.title()}: {len(files)} files")

    print(f"\n🔐 Authentication System:")
    for key, value in findings["auth_system"].items():
        print(f"  {key}: {len(value) if isinstance(value, list) else value} occurrences")

    print(f"\n📡 API Endpoints Found: {len(findings['file_connections'].get('api_endpoints', []))}")

    print(f"\n⚙️  Environment Config:")
    env_info = findings["deployment_config"]
    print(f"  Config files: {len(env_info['env_files'])}")
    print(f"  Config variables: {len(env_info['config_vars'])}")

    print(f"\n🚨 CRITICAL ISSUES: {len(findings['critical_issues'])}")
    for issue in findings['critical_issues']:
        print(f"  - {issue}")

    print(f"\n⚠️  MAJOR ISSUES: {len(findings['major_issues'])}")
    for issue in findings['major_issues']:
        print(f"  - {issue}")

    print(f"\n🔍 MINOR ISSUES: {len(findings['minor_issues'])}")
    for issue in findings['minor_issues']:
        print(f"  - {issue}")


if __name__ == "__main__":
    main()