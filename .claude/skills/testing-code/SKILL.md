---
name: testing-code
description: Generates production-grade, framework-appropriate automated test suites that maximize correctness, reliability, maintainability, and coverage. Detects programming languages, selects optimal testing frameworks, creates separated test architecture, and implements comprehensive test patterns for functional behavior, edge cases, invalid inputs, exception handling, and boundary analysis.
license: Complete terms in LICENSE.txt
---

# Testing Code

This skill analyzes codebases to generate production-grade, framework-appropriate automated test suites that maximize correctness, reliability, maintainability, and coverage. The skill systematically detects programming languages, selects optimal testing frameworks, creates separated test architecture, and implements comprehensive test patterns following industry best practices.

## About Testing Code Skill

This skill provides automated testing capabilities by generating comprehensive test suites for any codebase. Think of it as a "testing assistant" that transforms Claude from a general-purpose agent into a specialized testing engineer equipped with procedural knowledge to create professional-grade automated tests.

### What This Skill Provides

1. **Language Detection** - Automatically identifies programming languages and ecosystems
2. **Framework Selection** - Chooses optimal testing frameworks based on project type
3. **Test Architecture** - Creates organized, separated test directory structures
4. **Comprehensive Testing** - Generates functional, edge case, invalid input, and exception handling tests
5. **CI/CD Integration** - Configures tests for professional deployment pipelines

## Overview

## When to Use This Skill

This skill should be used when:
- Implementing automated testing for new or existing codebases
- Detecting the optimal testing framework for a specific programming language
- Creating organized, separated test architecture following best practices
- Generating comprehensive test coverage with functional, edge case, invalid input, and exception handling tests
- Establishing professional-grade test infrastructure for CI/CD pipelines
- Ensuring high-quality test suites with AAA pattern, parameterized tests, and proper fixtures

## Language & Ecosystem Analysis

1. Automatically detect:
   - Programming language and version (if identifiable)
   - Project type (CLI tool, library, API service, OOP system, etc.)
   - Dependency manager (if present)

2. Select the most appropriate and industry-standard testing framework for that language.

   Examples (not limited to):
   - Python → pytest
   - C++ → Google Test (gtest)
   - Java → JUnit 5
   - JavaScript → Jest
   - TypeScript → Jest / Vitest
   - C# → xUnit / NUnit
   - Go → built-in testing package
   - PHP → PHPUnit
   - Ruby → RSpec

3. Justify framework choice based on:
   - Ecosystem compatibility
   - Community adoption
   - CI/CD integration
   - Maintainability and testability

## Test Architecture & Directory Structure

4. Create a completely separate test directory.

   - The test folder must be outside the main source directory.
   - If applicable, the test directory should exist at the same level as the project root directory.
   - Never mix test files with production source files.
   - Follow ecosystem naming conventions (e.g., tests/, test/, __tests__/).

5. Recommended directory structure:

   Example (if tests are outside the root source folder):

   workspace/
   ├── project-root/
   │   ├── src/
   │   ├── core/
   │   └── config files
   └── tests/
       ├── test_module1.*
       ├── test_module2.*
       └── setup/fixture files

   If outside-root separation is not applicable for the ecosystem,
   explain clearly and place tests in the most professional standard location.

6. Ensure:
   - Clear separation of concerns
   - Scalable structure
   - Modular test grouping
   - Proper import configuration (include instructions if path adjustments are needed)

## General Testing Pattern Applied

For every class, function, or module, systematically validate:

1. Functional Behavior
   - Correct outputs for valid inputs
   - Expected return types
   - Correct state transitions (if stateful)

2. Edge Cases
   - Empty input
   - Null / None values
   - Zero values
   - Minimum and maximum boundaries

3. Invalid Inputs
   - Wrong data types
   - Missing arguments
   - Out-of-range values
   - Malformed input

4. Exception Handling
   - Proper exception raising
   - Correct error messages
   - Graceful failure handling

5. Boundary Value Analysis
   - Off-by-one conditions
   - Threshold limits
   - Range validations

6. External Dependencies (if applicable)
   - File I/O
   - Database access
   - Network/API calls
   - Environment variables

   → Use mocking/stubbing to ensure isolation and determinism.

7. Determinism & Stability
   - No reliance on randomness unless controlled
   - No shared hidden state
   - Independent and isolated tests

## Test Generation Standards

Follow professional best practices:

- Use AAA pattern (Arrange, Act, Assert)
- Use parameterized tests where appropriate
- Use fixtures/setup/teardown correctly
- Maintain clear and descriptive test names:
    test_<unit>_<scenario>_<expected_behavior>
- Avoid redundant or overlapping tests
- Ensure readability and maintainability

Aim for high logical coverage.
- Highlight uncovered areas
- Identify high-risk logic
- Suggest minimal refactoring if testability is needed

## Skill Usage Process

1. **Analyze the Codebase**: Examine the target codebase to detect language, framework, and project structure
2. **Select Testing Framework**: Choose the most appropriate testing framework based on ecosystem analysis
3. **Design Architecture**: Create a separated test directory structure following best practices
4. **Generate Tests**: Create comprehensive test suites covering all required patterns
5. **Provide Execution Commands**: Deliver dependency installation, execution, and coverage commands

## Professional CI/CD Integration

Assume integration with a professional CI/CD pipeline:
- Test execution commands that work in CI environments
- Coverage reporting tools appropriate for the chosen framework
- Output formats compatible with CI/CD systems
- Parallelization capabilities when available in the framework

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform test generation operations.

**Examples:**
- `generate_tests.py` - Automated script to detect project types and generate appropriate test files
- `validate_test_coverage.py` - Script to check test coverage and provide feedback
- `test_framework_detector.py` - Script to identify the optimal testing framework for a given codebase

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs test automation, framework detection, or test suite generation.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples:**
- `testing_patterns.md` - Comprehensive guide to testing patterns for different languages
- `framework_comparison.md` - Detailed comparison of testing frameworks across ecosystems
- `best_practices.md` - Industry best practices for test architecture and maintenance
- `ci_integration.md` - Guidelines for CI/CD integration with different testing frameworks

**Appropriate for:** In-depth documentation, testing guidelines, comprehensive frameworks, or any detailed information that Claude should reference while working on test generation.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples:**
- Test template files for different frameworks
- Sample test configurations (.yaml, .json, .toml) for various testing tools
- Boilerplate test directory structures
- Coverage configuration templates

**Appropriate for:** Templates, boilerplate code, configuration files, or any files meant to be copied or used in the final test output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.