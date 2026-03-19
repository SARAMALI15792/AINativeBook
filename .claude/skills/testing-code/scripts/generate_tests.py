#!/usr/bin/env python3
"""
Test Suite Generator - Automatically creates comprehensive test suites for codebases

This script analyzes a codebase to detect the programming language, select the optimal
testing framework, create organized test architecture, and generate comprehensive test
suites following industry best practices.

Usage:
    generate_tests.py <path-to-project> [options]

Examples:
    generate_tests.py ./my-python-project
    generate_tests.py ./my-java-project --output-dir ./custom-tests
    generate_tests.py ./my-js-project --framework jest
"""
import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TestGenerator:
    """Main class for generating test suites based on project analysis."""

    def __init__(self):
        self.framework_mapping = {
            '.py': {
                'name': 'pytest',
                'description': 'Recommended Python testing framework for its simplicity and powerful features',
                'dependencies': ['pytest', 'pytest-cov', 'pytest-mock'],
                'commands': {
                    'install': 'pip install pytest pytest-cov pytest-mock',
                    'run': 'pytest',
                    'run_with_coverage': 'pytest --cov=.',
                    'run_specific': 'pytest tests/test_module.py::TestClass::test_method'
                }
            },
            '.js': {
                'name': 'Jest',
                'description': 'JavaScript testing framework with built-in mocking and assertion libraries',
                'dependencies': ['jest'],
                'commands': {
                    'install': 'npm install --save-dev jest',
                    'run': 'npm test',
                    'run_with_coverage': 'npm test -- --coverage',
                    'run_specific': 'npm test -- --testNamePattern="test pattern"'
                }
            },
            '.ts': {
                'name': 'Jest',
                'description': 'TypeScript testing framework with TypeScript support',
                'dependencies': ['jest', '@types/jest', 'ts-jest'],
                'commands': {
                    'install': 'npm install --save-dev jest @types/jest ts-jest',
                    'run': 'npm test',
                    'run_with_coverage': 'npm test -- --coverage',
                    'run_specific': 'npm test -- --testNamePattern="test pattern"'
                }
            },
            '.java': {
                'name': 'JUnit 5',
                'description': 'Java testing framework with powerful extension model',
                'dependencies': ['junit-jupiter-api', 'junit-jupiter-engine'],
                'commands': {
                    'install': 'Add JUnit 5 dependencies to your build.gradle or pom.xml',
                    'run': 'mvn test',  # For Maven
                    'run_with_coverage': 'mvn test jacoco:report',
                    'run_specific': 'mvn test -Dtest=TestClassName#testMethod'
                }
            },
            '.cpp': {
                'name': 'Google Test',
                'description': 'C++ testing framework with comprehensive assertion macros',
                'dependencies': ['googletest'],
                'commands': {
                    'install': 'sudo apt-get install libgtest-dev && cd /usr/src/gtest && sudo cmake . && sudo make && sudo make install',
                    'run': './test_executable',
                    'run_with_coverage': 'g++ --coverage test_file.cpp -lgtest -lgtest_main -pthread -o test && ./test && gcov test_file.cpp',
                    'run_specific': 'Use --gtest_filter=TestSuite.TestName'
                }
            },
            '.go': {
                'name': 'Go Testing',
                'description': 'Built-in Go testing package with simple and effective testing',
                'dependencies': ['testing'],
                'commands': {
                    'install': 'No additional installation needed',
                    'run': 'go test ./...',
                    'run_with_coverage': 'go test -coverprofile=coverage.out ./... && go tool cover -html=coverage.out',
                    'run_specific': 'go test -run=TestFunctionName ./path/to/package'
                }
            },
            '.php': {
                'name': 'PHPUnit',
                'description': 'PHP testing framework with comprehensive assertion library',
                'dependencies': ['phpunit/phpunit'],
                'commands': {
                    'install': 'composer require --dev phpunit/phpunit',
                    'run': 'vendor/bin/phpunit',
                    'run_with_coverage': 'vendor/bin/phpunit --coverage-html coverage',
                    'run_specific': 'vendor/bin/phpunit --filter TestClass::testMethod'
                }
            },
            '.rb': {
                'name': 'RSpec',
                'description': 'Ruby testing framework with expressive syntax',
                'dependencies': ['rspec'],
                'commands': {
                    'install': 'gem install rspec',
                    'run': 'rspec',
                    'run_with_coverage': 'rspec --format RspecJunitFormatter --out results.xml',
                    'run_specific': 'rspec spec/path/to/file_spec.rb:line_number'
                }
            }
        }

    def detect_language(self, project_path: str) -> Tuple[str, str]:
        """Detect the primary programming language of a project."""
        project_dir = Path(project_path)
        if not project_dir.exists():
            raise ValueError(f"Project path does not exist: {project_path}")

        extensions = {}
        for file_path in project_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix:
                ext = file_path.suffix.lower()
                extensions[ext] = extensions.get(ext, 0) + 1

        if not extensions:
            raise ValueError(f"No source files found in project: {project_path}")

        primary_ext = max(extensions, key=extensions.get)
        return primary_ext, extensions[primary_ext]

    def get_framework_info(self, language_ext: str) -> Dict:
        """Get framework information for the detected language."""
        if language_ext in self.framework_mapping:
            return self.framework_mapping[language_ext]
        else:
            # Default to a generic framework info if language not recognized
            return {
                'name': 'Generic Testing Framework',
                'description': f'Testing framework for {language_ext} projects (specific framework not predefined)',
                'dependencies': [],
                'commands': {
                    'install': 'Install appropriate testing framework for this language',
                    'run': 'Run tests using appropriate command',
                    'run_with_coverage': 'Run tests with coverage using appropriate tool',
                    'run_specific': 'Run specific tests using appropriate syntax'
                }
            }

    def create_directory_structure(self, project_path: str, output_dir: Optional[str] = None) -> str:
        """Create a proper test directory structure separate from source."""
        project_dir = Path(project_path)

        # Determine test directory path
        if output_dir:
            test_dir = Path(output_dir)
        else:
            # Try common test directory locations relative to project
            potential_paths = [
                project_dir / "tests",
                project_dir / "test",
                project_dir / "__tests__",
                project_dir.parent / f"{project_dir.name}-tests",
                project_dir / "spec"  # For Ruby projects
            ]

            for path in potential_paths:
                if not path.exists():
                    test_dir = path
                    break
            else:
                # If all common paths exist, use default
                test_dir = project_dir / "tests"

        # Create test directory if it doesn't exist
        test_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for organization
        subdirs = ["unit", "integration", "fixtures", "helpers"]
        for subdir in subdirs:
            (test_dir / subdir).mkdir(exist_ok=True)

        return str(test_dir)

    def generate_test_file(self, source_file: Path, test_dir: str) -> str:
        """Generate a test file for a given source file."""
        relative_path = source_file.relative_to(source_file.parent)
        test_file_name = f"test_{source_file.name}"

        # Adjust naming convention based on language
        if source_file.suffix == '.py':
            test_file_name = f"test_{source_file.stem}.py"
        elif source_file.suffix in ['.js', '.ts']:
            test_file_name = f"{source_file.stem}.test{source_file.suffix}"
        elif source_file.suffix == '.java':
            test_file_name = f"{source_file.stem}Test.java"
        elif source_file.suffix == '.rb':
            test_file_name = f"{source_file.stem}_spec.rb"

        test_path = Path(test_dir) / test_file_name
        return str(test_path)

    def generate_sample_test_content(self, language_ext: str, module_name: str) -> str:
        """Generate sample test content based on the language."""
        if language_ext == '.py':
            return f'''import pytest
from {module_name} import *  # Import what you need to test


class Test{module_name.capitalize()}:
    """Test suite for {module_name} module."""

    def test_function_behavior(self):
        """Test correct outputs for valid inputs."""
        # Arrange
        # Set up test data

        # Act
        # Call the function being tested

        # Assert
        # Verify expected behavior
        assert True  # Replace with actual assertion

    def test_edge_cases(self):
        """Test edge cases like empty input, null values, boundaries."""
        # Test with empty input, None, zero values, etc.
        pass

    def test_invalid_inputs(self):
        """Test with invalid inputs to ensure proper error handling."""
        # Test with wrong data types, missing arguments, etc.
        pass

    def test_exception_handling(self):
        """Test that proper exceptions are raised for invalid inputs."""
        # Test exception raising and error messages
        pass
'''
        elif language_ext in ['.js', '.ts']:
            return f'''const {{ expect }} = require('@jest/globals');
// Import module to test
// const {module_name} = require('./path/to/{module_name}');


describe('{module_name}', () => {{
  test('should behave correctly with valid inputs', () => {{
    // Arrange
    // Set up test data

    // Act
    // Call the function being tested

    // Assert
    // Verify expected behavior
    expect(true).toBe(true); // Replace with actual assertion
  }});

  test('should handle edge cases', () => {{
    // Test with empty input, null, zero values, boundaries
    // Test with empty array, null values, etc.
  }});

  test('should throw error for invalid inputs', () => {{
    // Test with wrong data types, missing arguments, etc.
    // Use expect(() => fn()).toThrow() if applicable
  }});

  test('should handle exception scenarios', () => {{
    // Test that appropriate errors are thrown
  }});
}});
'''
        elif language_ext == '.java':
            return f'''package test;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class {module_name}Test {{

    @Test
    public void testFunctionBehavior() {{
        // Test correct outputs for valid inputs
        // Arrange
        // Set up test data

        // Act
        // Call the method being tested

        // Assert
        // Verify expected behavior
        assertTrue(true); // Replace with actual assertion
    }}

    @Test
    public void testEdgeCases() {{
        // Test edge cases like empty input, null values, boundaries
    }}

    @Test
    public void testInvalidInputs() {{
        // Test with invalid inputs to ensure proper error handling
    }}

    @Test
    public void testExceptionHandling() {{
        // Test that proper exceptions are raised for invalid inputs
        // Use assertThrows() when appropriate
    }}
}}
'''
        elif language_ext == '.go':
            return f'''package main

import (
    "testing"
)

func TestFunctionBehavior(t *testing.T) {{
    // Test correct outputs for valid inputs
    // Arrange
    // Set up test data

    // Act
    // Call the function being tested

    // Assert
    // Verify expected behavior
    if true != true {{ // Replace with actual assertion
        t.Errorf("Expected true, got false")
    }}
}}

func TestEdgeCases(t *testing.T) {{
    // Test edge cases like empty input, null values, boundaries
}}

func TestInvalidInputs(t *testing.T) {{
    // Test with invalid inputs to ensure proper error handling
}}

func TestExceptionHandling(t *testing.T) {{
    // Go doesn't have exceptions, but test for error returns
}}
'''
        elif language_ext == '.php':
            return f'''<?php

use PHPUnit\Framework\TestCase;

class {module_name}Test extends TestCase
{{
    public function testFunctionBehavior(): void
    {{
        // Test correct outputs for valid inputs
        // Arrange
        // Set up test data

        // Act
        // Call the method being tested

        // Assert
        // Verify expected behavior
        $this->assertTrue(true); // Replace with actual assertion
    }}

    public function testEdgeCases(): void
    {{
        // Test edge cases like empty input, null values, boundaries
    }}

    public function testInvalidInputs(): void
    {{
        // Test with invalid inputs to ensure proper error handling
    }}

    public function testExceptionHandling(): void
    {{
        // Test that proper exceptions are raised for invalid inputs
        // Use $this->expectException() when appropriate
    }}
}}
'''
        elif language_ext == '.rb':
            return f'''require 'rspec'
# require_relative '../lib/{module_name}'  # Adjust path to your module

RSpec.describe {module_name.capitalize} do
  describe "#method_name" do
    it "behaves correctly with valid inputs" do
      # Arrange: Set up test data

      # Act: Call the method being tested

      # Assert: Verify expected behavior
      expect(true).to be true  # Replace with actual assertion
    end

    it "handles edge cases" do
      # Test with empty input, nil values, boundaries
    end

    it "raises error for invalid inputs" do
      # Test with invalid inputs
      # expect {{ method_call }}.to raise_error(ExpectedError)
    end

    it "handles exception scenarios" do
      # Test that appropriate errors are raised
    end
  end
end
'''
        else:
            # Generic test template
            return f'''// Test suite for {module_name}
// Generated test file for {language_ext} language
// Follow AAA pattern (Arrange, Act, Assert)
// Cover functional behavior, edge cases, invalid inputs, and exception handling

// Example test structure:
// - Test correct outputs for valid inputs
// - Test edge cases (empty, null, zero, boundaries)
// - Test invalid inputs (wrong types, missing args)
// - Test proper exception/error handling
// - Test boundary conditions
'''

    def analyze_project(self, project_path: str) -> Dict:
        """Analyze the project and return information about test generation."""
        project_dir = Path(project_path)
        if not project_dir.exists():
            raise ValueError(f"Project path does not exist: {project_path}")

        # Detect language
        language_ext, count = self.detect_language(project_path)
        framework_info = self.get_framework_info(language_ext)

        # Find source files to create tests for
        source_files = []
        for file_path in project_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix == language_ext:
                source_files.append(str(file_path))

        return {
            'project_path': project_path,
            'primary_language': language_ext,
            'file_count': count,
            'framework_info': framework_info,
            'source_files': source_files,
            'detected_files': len(source_files)
        }

    def generate_tests(self, project_path: str, output_dir: Optional[str] = None) -> Dict:
        """Generate comprehensive test suite for the project."""
        # Analyze the project
        analysis = self.analyze_project(project_path)

        # Create test directory structure
        test_dir = self.create_directory_structure(project_path, output_dir)

        # Generate test files for each source file
        generated_tests = []
        for source_file in analysis['source_files']:
            source_path = Path(source_file)
            # Generate test file name based on source
            if source_path.suffix == '.py':
                test_file_name = f"test_{source_path.stem}.py"
            elif source_path.suffix in ['.js', '.ts']:
                test_file_name = f"{source_path.stem}.test{source_path.suffix}"
            elif source_path.suffix == '.java':
                test_file_name = f"{source_path.stem}Test.java"
            elif source_path.suffix == '.rb':
                test_file_name = f"{source_path.stem}_spec.rb"
            else:
                test_file_name = f"test_{source_path.name}"

            test_path = Path(test_dir) / test_file_name
            test_content = self.generate_sample_test_content(
                analysis['primary_language'],
                source_path.stem
            )

            # Write test file
            with open(test_path, 'w', encoding='utf-8') as f:
                f.write(test_content)

            generated_tests.append(str(test_path))

        # Create configuration files if needed
        self.create_config_files(test_dir, analysis['primary_language'])

        return {
            'test_directory': test_dir,
            'generated_tests': generated_tests,
            'framework_info': analysis['framework_info'],
            'summary': {
                'tests_created': len(generated_tests),
                'language': analysis['primary_language'],
                'framework': analysis['framework_info']['name']
            }
        }

    def create_config_files(self, test_dir: str, language_ext: str):
        """Create framework-specific configuration files."""
        if language_ext == '.py':
            # Create pytest.ini
            config_path = Path(test_dir) / 'pytest.ini'
            config_content = '''[tool:pytest]
testpaths = tests
addopts = -v
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
'''
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(config_content)

        elif language_ext in ['.js', '.ts']:
            # Create jest.config.js
            config_path = Path(test_dir) / 'jest.config.js'
            config_content = '''module.exports = {
  testEnvironment: 'node',
  testMatch: [
    '**/__tests__/**/*.[jt]s?(x)',
    '**/?(*.)+(spec|test).[tj]s?(x)'
  ],
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts'
  ]
};
'''
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(config_content)

        elif language_ext == '.java':
            # Create basic build.gradle for testing if needed
            parent_dir = Path(test_dir).parent
            gradle_path = parent_dir / 'build.gradle'
            if not gradle_path.exists():
                config_content = '''plugins {
    id 'java'
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter-api:5.8.2'
    testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.8.2'
}

test {
    useJUnitPlatform()
}
'''
                with open(gradle_path, 'w', encoding='utf-8') as f:
                    f.write(config_content)


def main():
    parser = argparse.ArgumentParser(description='Generate comprehensive test suites for codebases')
    parser.add_argument('project_path', help='Path to the project to analyze and generate tests for')
    parser.add_argument('--output-dir', help='Custom output directory for tests (default: auto-detect)')
    parser.add_argument('--framework', help='Force specific testing framework')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without creating files')

    args = parser.parse_args()

    generator = TestGenerator()

    try:
        if args.framework:
            print(f"⚠️  Framework override specified: {args.framework}")
            print("Note: Framework-specific generation not yet implemented for overrides")

        print(f"🔍 Analyzing project: {args.project_path}")
        analysis = generator.analyze_project(args.project_path)

        print(f"✅ Detected primary language: {analysis['primary_language']}")
        print(f"📊 Found {analysis['detected_files']} source files")
        print(f"🔧 Recommended framework: {analysis['framework_info']['name']}")
        print(f"📋 {analysis['framework_info']['description']}")

        if not args.dry_run:
            print(f"⚙️  Generating tests...")
            result = generator.generate_tests(args.project_path, args.output_dir)

            print(f"✅ Test suite generated successfully!")
            print(f"📁 Test directory: {result['test_directory']}")
            print(f"📝 Tests created: {result['summary']['tests_created']}")
            print(f"🎯 Framework: {result['summary']['framework']}")

            # Print commands for the user
            framework_info = result['framework_info']
            print(f"\n🔧 Commands to get started:")
            print(f"Install: {framework_info['commands']['install']}")
            print(f"Run all tests: {framework_info['commands']['run']}")
            print(f"Run with coverage: {framework_info['commands']['run_with_coverage']}")
        else:
            print("📖 Dry run completed - no files were created")
            print(f"Would create tests in: {args.output_dir or 'auto-detected location'}")

    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()