---
id: 005
title: Create testing-code skill following skill-creator pattern
stage: general
date: 2026-02-25
surface: agent
model: if/qwen3-coder-plus
feature: none
branch: main
user: saram
command: Create testing-code skill
labels: ["skill", "testing", "automation", "framework"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - C:\Users\saram\OneDrive\Desktop\physicalhumoniodbook\.claude\skills\engineering\testing-code\SKILL.md
  - C:\Users\saram\OneDrive\Desktop\physicalhumoniodbook\.claude\skills\engineering\testing-code\scripts\generate_tests.py
  - C:\Users\saram\OneDrive\Desktop\physicalhumoniodbook\.claude\skills\engineering\testing-code\references\testing_patterns.md
  - C:\Users\saram\OneDrive\Desktop\physicalhumoniodbook\.claude\skills\engineering\testing-code\assets\test_templates.md
  - C:\Users\saram\OneDrive\Desktop\physicalhumoniodbook\.claude\skills\engineering\testing-code\README.md
tests: []
---

## Prompt

Generate an skills and use the pattern of the @.claude/skills/skill-creator\ complety based on this format create an skill of name the testing-code and it make sure that it follow the pattern of skillcratro file and now use these intructions to crate skills on the attch apattern :You are a Principal Software Test Engineer specializing in automated testing, test architecture, and cross-language code quality automation.

Your mission is to analyze the provided codebase and generate a production-grade, framework-appropriate automated test suite that maximizes correctness, reliability, maintainability, and coverage.

=====================================================
PHASE 1 — LANGUAGE & ECOSYSTEM ANALYSIS
=====================================================

1. Automatically detect:
   - Programming language
   - Language version (if identifiable)
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

3. Briefly justify the framework choice based on:
   - Ecosystem compatibility
   - Community adoption
   - CI/CD integration
   - Maintainability

=====================================================
PHASE 2 — TEST ARCHITECTURE & DIRECTORY STRUCTURE
=====================================================

4. Create a completely separate test directory.

   - The test folder must be outside the main source directory.
   - If applicable, the test directory should exist at the same level as the project root directory.
   - Never mix test files with production source files.
   - Follow ecosystem naming conventions (e.g., tests/, test/, __tests__/).

5. Provide a recommended directory structure.

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

=====================================================
PHASE 3 — GENERAL TESTING PATTERN (WHAT TO TEST)
=====================================================

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

=====================================================
PHASE 4 — TEST GENERATION STANDARDS
=====================================================

7. Follow professional best practices:

   - Use AAA pattern (Arrange, Act, Assert)
   - Use parameterized tests where appropriate
   - Use fixtures/setup/teardown correctly
   - Maintain clear and descriptive test names:
       test_<unit>_<scenario>_<expected_behavior>
   - Avoid redundant or overlapping tests
   - Ensure readability and maintainability

8. Aim for high logical coverage.
   - Highlight uncovered areas
   - Identify high-risk logic
   - Suggest minimal refactoring if testability is weak

=====================================================
PHASE 5 — DELIVERY FORMAT
=====================================================

Provide the final output in the following structured format:

A. Summary Analysis
B. Detected Language & Framework
C. Justification of Framework Selection
D. Recommended Directory Structure (with outside-root separation if applicable)
E. General Testing Pattern Applied
F. Full Production-Ready Test Suite Code
G. Dependency Installation Commands
H. Test Execution Commands
I. Coverage Commands (if supported)

=====================================================
CONSTRAINTS
=====================================================

- Do NOT modify production code unless absolutely necessary.
- If refactoring is required, explain clearly and minimally.
- Maintain strict separation between production and test code.
- Assume integration with a professional CI/CD pipeline.
- Produce clean, scalable, maintainable test architecture.

Now analyze the provided codebase and generate a complete, well-architected, industry-standard automated test suite accordingly.

## Response snapshot

I have successfully created the testing-code skill following the skill-creator pattern. The skill implements a Principal Software Test Engineer capability for automated testing, test architecture, and cross-language code quality automation.

## Files Created:

1. `SKILL.md` - Main skill definition with comprehensive description and usage guidelines
2. `scripts/generate_tests.py` - Complete Python script that analyzes codebases and generates test suites
3. `references/testing_patterns.md` - Comprehensive testing patterns guide across languages
4. `assets/test_templates.md` - Configuration templates for various testing frameworks
5. `README.md` - Documentation of what was created

## Key Features Implemented:

- **Automatic Language Detection**: Detects primary programming language by file extensions
- **Framework Selection**: Selects optimal testing frameworks (pytest, Jest, JUnit, etc.)
- **Separated Architecture**: Creates test directories separate from source code
- **Comprehensive Coverage**: Generates tests for functional behavior, edge cases, invalid inputs, and exception handling
- **Cross-Language Support**: Python, JavaScript/TypeScript, Java, C++, Go, PHP, Ruby
- **CI/CD Integration**: Configures tests for professional CI/CD pipelines
- **AAA Pattern**: Uses Arrange, Act, Assert pattern for clear test structure

The skill follows the exact pattern of the skill-creator and implements all the comprehensive testing requirements specified in the instructions.

## Outcome

- ✅ Impact: Created a comprehensive testing skill that follows the skill-creator pattern
- 🧪 Tests: No tests run (skill creation task)
- 📁 Files: 5 files created across appropriate directories (SKILL.md, script, references, assets, README)
- 🔁 Next prompts: Ready to use the testing-code skill for automated test generation
- 🧠 Reflection: Successfully implemented a complex multi-component skill following established patterns

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A for this skill creation task
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test the skill with a sample codebase to validate functionality