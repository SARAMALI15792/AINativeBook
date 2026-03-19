# Testing Patterns and Best Practices Reference

## Overview

This document provides comprehensive guidance on testing patterns and best practices across different programming languages and ecosystems. It serves as a reference for implementing effective, maintainable, and comprehensive test suites.

## Testing Patterns by Category

### Functional Behavior Testing

**Purpose**: Validate that functions and modules behave as expected with correct inputs.

**Best Practices**:
- Test with valid inputs to ensure correct outputs
- Verify return types match expectations
- Check state transitions in stateful objects
- Validate business logic implementation

**Examples**:
```
# Python
def test_calculate_total():
    # Arrange
    items = [10, 20, 30]

    # Act
    result = calculate_total(items)

    # Assert
    assert result == 60
    assert isinstance(result, int)
```

### Edge Case Testing

**Purpose**: Handle boundary conditions and unusual input scenarios.

**Common Edge Cases**:
- Empty collections (arrays, lists, strings)
- Null or None values
- Zero values
- Minimum and maximum numeric values
- Single-element collections
- Very large inputs

**Examples**:
```
# Python
def test_calculate_total_empty_list():
    # Edge case: empty list
    result = calculate_total([])
    assert result == 0
```

### Invalid Input Testing

**Purpose**: Ensure graceful handling of incorrect inputs.

**Types to Test**:
- Wrong data types
- Missing required parameters
- Out-of-range values
- Malformed input formats
- Invalid state transitions

**Examples**:
```
# Python
def test_calculate_total_invalid_type():
    # Invalid type should raise TypeError
    with pytest.raises(TypeError):
        calculate_total("not a list")
```

### Exception Handling Testing

**Purpose**: Verify proper error handling and error message quality.

**Best Practices**:
- Test that appropriate exceptions are raised
- Verify exception messages are informative
- Check that exceptions are properly propagated
- Ensure cleanup code runs in exception scenarios

**Examples**:
```
# Python
def test_divide_by_zero_raises_exception():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)
```

## Language-Specific Patterns

### Python Testing Patterns

**Framework**: pytest

**Naming Convention**: `test_*.py`, `*_test.py`, or `test_*.py`

**Fixtures**:
```python
@pytest.fixture
def sample_data():
    return {"key": "value", "list": [1, 2, 3]}

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"
```

**Parameterized Tests**:
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16)
])
def test_square(input, expected):
    assert square(input) == expected
```

### JavaScript/TypeScript Testing Patterns

**Framework**: Jest

**Naming Convention**: `*.test.js`, `*.spec.js`, `*.test.ts`, `*.spec.ts`

**Async Testing**:
```javascript
test('fetches data asynchronously', async () => {
  const data = await fetchData();
  expect(data).toEqual(expectedData);
});
```

**Mocking**:
```javascript
jest.mock('./api');
test('calls API with correct parameters', () => {
  const api = require('./api');
  api.getData.mockReturnValue({ id: 1 });

  const result = processData();
  expect(api.getData).toHaveBeenCalledWith();
});
```

### Java Testing Patterns

**Framework**: JUnit 5

**Naming Convention**: `*Test.java`

**Parameterized Tests**:
```java
@ParameterizedTest
@ValueSource(ints = {1, 2, 3})
void testMethod(int argument) {
    assertTrue(argument > 0);
}
```

**Test Fixtures**:
```java
@BeforeEach
void setUp() {
    // Initialize test objects
    calculator = new Calculator();
}

@AfterEach
void tearDown() {
    // Clean up after each test
    calculator = null;
}
```

## Test Organization and Structure

### AAA Pattern (Arrange, Act, Assert)

**Arrange**: Set up test data, inputs, and mock objects
**Act**: Execute the method/function under test
**Assert**: Verify the expected outcomes

### Test Hierarchy and Organization

```
tests/
├── unit/
│   ├── services/
│   ├── models/
│   └── utils/
├── integration/
│   ├── api/
│   ├── database/
│   └── external/
├── fixtures/
│   ├── sample_data.json
│   └── mock_objects.py
└── helpers/
    ├── test_utils.py
    └── mock_factories.py
```

## Coverage and Quality Metrics

### Coverage Requirements

- **Minimum Line Coverage**: 80%
- **Branch Coverage**: 70% for complex conditional logic
- **Function Coverage**: 90% for public methods

### Quality Indicators

- **Test Independence**: Each test runs in isolation
- **Deterministic Results**: Tests produce consistent results
- **Fast Execution**: Tests run quickly (under 100ms when possible)
- **Clear Failure Messages**: Failures clearly indicate what went wrong

## Advanced Testing Techniques

### Property-Based Testing

Test properties that should hold for all inputs of a certain type rather than specific examples.

### Fuzz Testing

Automated testing with random inputs to find edge cases and unexpected behaviors.

### Contract Testing

Ensure that components interact correctly by testing their contracts/expectations.

## CI/CD Integration

### Test Execution Order

1. Fast unit tests first
2. Integration tests second
3. End-to-end tests last

### Parallelization Strategies

- Run test files in parallel
- Run test classes in parallel
- Run individual tests in parallel (for long-running tests)

### Reporting and Monitoring

- Publish coverage reports
- Track test execution time trends
- Alert on test failures or performance regressions

## Anti-Patterns to Avoid

### Test Smells

- **Fragile Tests**: Tests that break frequently due to minor changes
- **Slow Tests**: Tests that take too long to run
- **Dependent Tests**: Tests that depend on execution order or shared state
- **Mystery Guests**: Tests that don't clearly show what they're testing
- **Mockery**: Overuse of mocks that don't test real behavior

### Common Mistakes

- Testing implementation details instead of behavior
- Sharing test state between test methods
- Testing private methods directly
- Having tests that are too broad or too narrow
- Not testing error conditions