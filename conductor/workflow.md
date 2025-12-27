# Development Workflow

## Test-Driven Development (TDD)

This project follows TDD principles. Every feature and bug fix should follow this cycle:

### The TDD Cycle

```
1. RED    - Write a failing test that defines desired behavior
2. GREEN  - Write minimal code to make the test pass
3. REFACTOR - Improve code quality while keeping tests green
```

### TDD Implementation Steps

For each task:

1. **Understand Requirements**
   - Review the spec and acceptance criteria
   - Identify edge cases and error conditions
   - List all behaviors that need testing

2. **Write Failing Tests First**
   - Create test file if it doesn't exist
   - Write test for the simplest case first
   - Run test to confirm it fails (RED)
   - Commit the failing test with message: `test: add failing test for <feature>`

3. **Implement Minimal Solution**
   - Write just enough code to pass the test
   - Don't anticipate future needs
   - Run test to confirm it passes (GREEN)
   - Commit: `feat: implement <feature> to pass test`

4. **Refactor**
   - Improve code structure and readability
   - Remove duplication
   - Ensure all tests still pass
   - Commit: `refactor: improve <component>`

5. **Repeat**
   - Add next test case
   - Continue until all acceptance criteria met

## Test Organization

```
tests/
├── unit/           # Fast, isolated tests (mock external deps)
├── integration/    # Tests with real dependencies
└── fixtures/       # Shared test data and cassettes
```

## Testing Commands

```bash
# Run all tests
pytest openbb_platform

# Run unit tests only
pytest openbb_platform -m "not integration"

# Run integration tests only
pytest openbb_platform -m integration

# Run specific provider tests
pytest openbb_platform/providers/yfinance/tests/

# Generate unit tests for fetchers
python openbb_platform/providers/tests/utils/unit_tests_generator.py

# Record test fixtures
pytest <path_to_test_file> --record=all
```

## Commit Message Convention

Format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `test`: Adding or updating tests
- `refactor`: Code restructuring without behavior change
- `docs`: Documentation only
- `chore`: Build, tooling, or maintenance

## Branch Naming

- `feature/feature-name` - New features
- `hotfix/hotfix-name` - Bug fixes

PRs target the `develop` branch.

## Quality Gates

Before merging:
- [ ] All tests pass
- [ ] No linting errors (`pre-commit run --all-files`)
- [ ] Type checking passes (`mypy`)
- [ ] Code review approved
- [ ] Documentation updated if needed

## Code Review Checklist

- Does it follow TET pattern for fetchers?
- Are all new functions tested?
- Are error cases handled?
- Is the code readable without excessive comments?
- Does it follow existing patterns in the codebase?
