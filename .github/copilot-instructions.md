# Copilot Custom Instructions for my_todo_lib Project

---
applyTo: "**"
---

## Project Overview

**Project**: my_todo_lib - A comprehensive Python to-do list library with auto-save persistence, task management, and interactive CLI.

**Purpose**: Provide a robust, well-tested, and user-friendly task/to-do list management library.

---

## Code Style & Standards

### Python Standards
- **Style Guide**: PEP 8 compliance (enforced by flake8, black)
- **Line Length**: Maximum 100 characters
- **Indentation**: 4 spaces per level
- **Type Hints**: Required for all function signatures and class methods
- **Docstrings**: Google-style docstrings for all public methods and classes
- **Comments**: Clear, concise comments explaining "why", not "what"

### Naming Conventions
- **Classes**: PascalCase (e.g., `TaskManager`, `TaskList`)
- **Functions/Methods**: snake_case (e.g., `get_tasks()`, `move_task_to_list()`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_STORAGE_PATH`)
- **Private Members**: Prefix with underscore (e.g., `_internal_method()`)
- **Avoid**: Single letter variable names (except in comprehensions)

---

## Architecture & Components

### Core Library Structure
```
my_todo_lib/
├── __init__.py          (Main package exports)
├── core/
│   ├── __init__.py
│   ├── task.py          (Task class - represents individual task)
│   ├── task_list.py     (TaskList class - collection of tasks)
│   ├── list_container.py (ListContainer class - collection of lists)
│   ├── constants.py     (Constants - defaults, limits)
│   └── ordering.py      (Ordering utility - task ordering logic)
├── storage/
│   ├── __init__.py
│   ├── base_storage.py  (BaseStorage abstract class)
│   └── json_storage.py  (JSONStorage - persistent storage)
└── manager.py           (TaskManager - main API, orchestrates components)
```

### Key Components & Responsibilities

1. **Task**: Represents a single task with title, description, status, priority
2. **TaskList**: Contains tasks, has name and description
3. **ListContainer**: Contains TaskLists, manages all lists
4. **TaskManager**: Main API, orchestrates all components, handles auto-save
5. **JSONStorage**: Persists data to JSON file
6. **Constants**: Defines limits and defaults (max lists, max tasks, etc.)
7. **Ordering**: Handles task ordering (creation date, priority, custom)

---

## Coding Requirements

### 1. Testing Requirements
- **Test Framework**: pytest with pytest-cov
- **Coverage Target**: Minimum 80% code coverage
- **Test Location**: `tests/` directory
- **Naming**: `test_<component>.py` (e.g., `test_manager.py`)
- **All Methods**: Must have corresponding unit tests
- **Error Cases**: Test both success and failure scenarios
- **No Skipped Tests**: All tests must be active (no `@pytest.mark.skip`)

### 2. Error Handling
- **Validation**: Validate all inputs at function entry
- **Clear Messages**: Exceptions must have descriptive messages
- **Type Checking**: Use type hints and validate types
- **Error Types**: Use appropriate exception types (ValueError, KeyError, etc.)
- **No Silent Failures**: Always raise or log errors, never silently ignore

### 3. Documentation
- **Docstrings**: Google-style format for all public functions/classes
- **README**: Keep updated with latest features and examples
- **FEATURE_*.md**: Create for major features (e.g., `MOVE_TASK_FEATURE.md`)
- **Examples**: Provide working example scripts in `examples/` directory
- **Comments**: Explain complex logic, edge cases, and design decisions

### 4. Auto-Save Implementation
- **When to Save**: After every state-changing operation
- **Save Method**: Call `self.save()` in TaskManager after mutations
- **Location**: Data persisted to `~/.my_todo_lib/tasks.json`
- **Format**: Pretty-printed JSON (indent=2) for readability
- **Backup**: Create `.backup` file before overwriting

---

## Feature Implementation Checklist

When implementing new features, follow this checklist:

### Planning Phase
- [ ] Define feature requirements clearly
- [ ] Plan component changes
- [ ] Identify error cases
- [ ] Design test scenarios

### Implementation Phase
- [ ] Add/modify core method in appropriate component
- [ ] Add type hints to all functions
- [ ] Add docstring (Google-style)
- [ ] Implement error handling with clear messages
- [ ] Call `self.save()` after state changes (for TaskManager)
- [ ] Add CLI menu option in `examples/interactive_cli.py` if user-facing

### Testing Phase
- [ ] Write unit tests (success cases)
- [ ] Write unit tests (error cases)
- [ ] Write integration test (real-world scenario)
- [ ] Achieve >80% coverage for new code
- [ ] All 142+ tests passing
- [ ] Run locally: `pytest tests/ -v --cov=my_todo_lib`

### CI/CD Phase
- [ ] Commit with descriptive message
- [ ] Push to GitHub
- [ ] GitHub Actions runs automatically
- [ ] Tests pass on Python 3.9, 3.10, 3.11
- [ ] Linting passes (flake8, black, pylint)
- [ ] Coverage report uploads to Codecov

### Documentation Phase
- [ ] Update README with new feature
- [ ] Create FEATURE_*.md if major
- [ ] Add example script demonstrating feature
- [ ] Update API documentation
- [ ] Add comments explaining complex parts

---

## Git Workflow

### Commit Messages
Format: `[category] Short description of change`

Categories:
- `[feature]` - New feature (e.g., `[feature] Add move task to list functionality`)
- `[fix]` - Bug fix (e.g., `[fix] Handle edge case in task priority`)
- `[refactor]` - Code restructuring (e.g., `[refactor] Simplify TaskManager initialization`)
- `[docs]` - Documentation only (e.g., `[docs] Add API documentation`)
- `[test]` - Test additions (e.g., `[test] Add 6 tests for move_task feature`)
- `[ci]` - CI/CD changes (e.g., `[ci] Add GitHub Actions workflow`)

### Detailed Messages
After category and title, add details:
```
[feature] Add move task to list functionality

- Adds move_task_to_list() method to TaskManager
- Preserves all task data during move
- Validates source/target lists exist
- Prevents moving to same list
- Includes 6 unit tests (all passing)
- Tested with real tasks, verified auto-save
- Updated interactive CLI with menu option
- Total tests now: 142 (100% pass rate)
```

### Branch Strategy
- **Main Branch**: `master` (production-ready)
- **Feature Branch**: `feature/<feature-name>`
- **Bugfix Branch**: `bugfix/<bug-name>`
- All changes via commits (no direct edits)

---

## Testing Strategy

### Test Structure
```python
import pytest
from my_todo_lib.manager import TaskManager

class TestFeatureName:
    """Test suite for feature_name functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        self.manager = TaskManager()
    
    def test_success_case(self):
        """Test the happy path"""
        # Arrange
        
        # Act
        
        # Assert
    
    def test_error_case(self):
        """Test error handling"""
        with pytest.raises(ValueError):
            # Code that should raise
            pass
```

### Coverage Requirements
- **Minimum**: 80% overall coverage
- **Target**: 85%+ coverage
- **Components with Tests**:
  - Task: 27 tests
  - TaskList: 33 tests
  - ListContainer: 31 tests
  - Storage: 17 tests
  - Manager: 28+ tests
  - Total: 142+ tests

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=my_todo_lib --cov-report=html

# Run specific test file
pytest tests/test_manager.py -v

# Run specific test
pytest tests/test_manager.py::TestManager::test_move_task_to_list -v
```

---

## Code Quality Tools

### Linting & Formatting
- **flake8**: Style guide enforcement (max line 100 chars)
- **black**: Code formatter (maintains PEP 8)
- **pylint**: Code quality analysis

### Run Locally
```bash
# Check style
flake8 my_todo_lib/

# Auto-format code
black my_todo_lib/ tests/

# Code quality
pylint my_todo_lib/
```

### CI/CD Enforcement
All of these run automatically on every commit via GitHub Actions:
- Python 3.9, 3.10, 3.11 testing
- Linting checks
- Coverage reporting
- Test execution

---

## API & Core Methods

### TaskManager (Main API)
```python
# Task operations
task = create_task(list_id, title, description, priority)
update_task(task_id, **kwargs)
delete_task(task_id)
get_task(task_id)
move_task_to_list(source_list_id, task_id, target_list_id)

# List operations
task_list = create_list(name, description)
update_list(list_id, **kwargs)
delete_list(list_id)
get_list(list_id)

# Container operations
get_all_lists()
get_all_tasks_across_lists()
get_list_count()

# Persistence
save()
load()
```

### Error Handling Pattern
```python
def method_name(self, param):
    """Method description.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
        
    Raises:
        ValueError: If validation fails
        KeyError: If resource not found
    """
    # Validate inputs
    if not param:
        raise ValueError("param cannot be empty")
    
    # Check resource exists
    if param not in self.resources:
        raise KeyError(f"Resource '{param}' not found")
    
    # Perform operation
    result = self._do_operation(param)
    
    # Save if mutating
    self.save()
    
    return result
```

---

## File Organization Best Practices

### New Feature Files
- Core logic: Add/modify in `my_todo_lib/` component
- Tests: Add in `tests/test_<component>.py`
- CLI: Add menu option in `examples/interactive_cli.py`
- Example: Create `examples/example_<feature>.py` if complex
- Docs: Create `FEATURE_<NAME>.md` in root for major features

### Documentation Files
- Feature docs: `FEATURE_*.md` (e.g., `FEATURE_MOVE_TASK.md`)
- Setup guides: `SETUP_GUIDE.md`
- API docs: `API_DOCUMENTATION.md`
- CI/CD docs: `CI_CD_GUIDE.md`
- Guidelines: `PROJECT_GUIDELINES.md`

---

## Common Patterns

### Creating a New Task
```python
manager = TaskManager()
new_list = manager.create_list("My List", "Description")
task = manager.create_task(
    list_id=new_list.id,
    title="Buy groceries",
    description="Milk, eggs, bread",
    priority=1
)
```

### Moving a Task
```python
source_list_id = "list_001"
task_id = "task_001"
target_list_id = "list_002"

moved_task = manager.move_task_to_list(
    source_list_id=source_list_id,
    task_id=task_id,
    target_list_id=target_list_id
)
```

### Error Handling in CLI
```python
try:
    result = manager.move_task_to_list(source, task_id, target)
    print(f"✅ Task moved: {result.title}")
except ValueError as e:
    print(f"❌ Error: {str(e)}")
except KeyError as e:
    print(f"❌ Not found: {str(e)}")
```

---

## Performance Considerations

### Current Implementation
- **Data Structure**: In-memory objects with JSON persistence
- **Save Timing**: After every mutation (auto-save)
- **Load Timing**: On first TaskManager initialization
- **Scale**: Tested with 1000+ tasks, 50+ lists (performs well)

### Optimization Guidelines
- Don't create unnecessary copies of objects
- Use list comprehensions instead of loops where cleaner
- Cache frequently accessed data where appropriate
- Profile before optimizing

---

## Communication Style in Code

### Comments & Documentation
```python
# ✅ GOOD: Explains WHY
# We filter completed tasks first to show progress to user quickly
completed = [t for t in tasks if t.status == "completed"]

# ❌ BAD: States the obvious
# Filter tasks for completed status
completed = [t for t in tasks if t.status == "completed"]
```

### Variable Names
```python
# ✅ GOOD: Clear, descriptive
tasks_by_priority = sorted(tasks, key=lambda t: t.priority)

# ❌ BAD: Unclear abbreviations
tsk_by_pr = sorted(tasks, key=lambda t: t.priority)
```

### Function Names
```python
# ✅ GOOD: Verb-based, clear intent
def move_task_to_list(self, source_list_id, task_id, target_list_id):
    pass

# ❌ BAD: Unclear what it does
def transfer(self, src, tid, tgt):
    pass
```

---

## When to Ask for Help (Copilot Guidance)

### Good Use Cases
- Implementing a new feature following existing patterns
- Writing comprehensive test cases
- Creating documentation
- Refactoring code for clarity
- Debugging failing tests
- Optimizing performance

### Ask Me For
- Feature requirements clarification
- Architecture decisions for complex features
- Merge conflict resolution
- Security considerations
- Major refactoring decisions

---

## Project Status & Next Steps

### ✅ Completed
- Core library (8 components, 142 tests, 100% pass rate)
- Auto-save persistence (JSON storage)
- Move task feature (with 6 unit tests)
- Interactive CLI (fully functional)
- GitHub Actions CI/CD (multi-version testing)
- Comprehensive documentation

### 🎯 Next Features (Optional)
- Recurring tasks
- Task reminders/notifications
- Task dependencies/subtasks
- Export to CSV/PDF
- Task templates
- Cloud sync
- Dark mode for CLI

---

## Quick Reference

| Tool | Command | Purpose |
|------|---------|---------|
| Tests | `pytest tests/ -v` | Run all tests |
| Coverage | `pytest tests/ --cov=my_todo_lib` | Check coverage |
| Lint | `flake8 my_todo_lib/` | Style check |
| Format | `black my_todo_lib/` | Auto-format |
| Git Push | `git push origin master` | Push to GitHub |
| View Logs | `git log --oneline` | See commits |

---

## References

- [Python PEP 8 Style Guide](https://pep8.org/)
- [Google Docstring Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Project README](../README.md)
- [API Documentation](../API_DOCUMENTATION.md)

---

**Last Updated**: 5 November 2025  
**Maintained By**: Development Team  
**Status**: ✅ Active & Current
