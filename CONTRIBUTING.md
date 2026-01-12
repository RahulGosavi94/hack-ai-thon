# Contributing to Hack-AI-Thon

Thank you for your interest in contributing to the Disruption Management & Passenger Care System! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. We pledge to:

- Be respectful of differing opinions and experiences
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

The following behaviors are considered unacceptable:

- Harassment or discrimination based on any protected characteristic
- Offensive comments related to gender, sexual orientation, race, religion, disability, etc.
- Harassment of any kind (public or private)
- Publishing private information without consent
- Other conduct which could reasonably be considered inappropriate

---

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- GitHub account
- Basic familiarity with Git and GitHub

### Fork & Clone

1. **Fork** the repository on GitHub
   ```bash
   # Click "Fork" button on https://github.com/RahulGosavi94/hack-ai-thon
   ```

2. **Clone** your fork locally
   ```bash
   git clone https://github.com/YOUR-USERNAME/hack-ai-thon.git
   cd hack-ai-thon
   ```

3. **Add upstream** remote
   ```bash
   git remote add upstream https://github.com/RahulGosavi94/hack-ai-thon.git
   ```

---

## Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Git Hooks (Optional)

```bash
# Copy pre-commit hooks
cp .githooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

### 4. Verify Setup

```bash
# Start Flask app
python3 app.py

# In another terminal, test API
curl http://localhost:5000/api/flights
```

---

## Making Changes

### Create a Feature Branch

Always create a new branch for your changes:

```bash
# Update main branch
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### Branch Naming Convention

- **Features:** `feature/short-description`
  - Example: `feature/add-email-notifications`
- **Bug fixes:** `fix/short-description`
  - Example: `fix/passenger-search-bug`
- **Documentation:** `docs/short-description`
  - Example: `docs/add-api-examples`
- **Refactoring:** `refactor/short-description`
  - Example: `refactor/improve-eligibility-logic`

### Make Your Changes

1. Modify files as needed
2. Test your changes locally
3. Ensure all tests pass
4. Update documentation if necessary

---

## Commit Guidelines

### Commit Message Format

Write clear, descriptive commit messages:

```
<type>: <subject>

<body>

<footer>
```

### Type

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, etc.)
- `refactor` - Code refactoring
- `test` - Adding/updating tests
- `chore` - Maintenance tasks

### Subject

- Use imperative mood ("add feature" not "added feature")
- Don't capitalize first letter
- No period at the end
- Maximum 50 characters

### Body

- Explain what and why, not how
- Wrap at 72 characters
- Use bullet points for multiple changes
- Reference issues when relevant (#123)

### Examples

**Good Commit:**
```
feat: add email notification system

- Implement email sending via SMTP
- Add email template system
- Create notification queue
- Add user email preferences

Closes #123
```

**Bad Commit:**
```
Fixed stuff
```

---

## Pull Request Process

### Before Submitting

1. **Update your branch:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test thoroughly:**
   ```bash
   # Run all tests
   python3 -m pytest tests/ -v
   
   # Test eligibility
   python3 test_eligibility.py
   
   # Test disruption detection
   python3 test_delay_reconciliation.py
   ```

3. **Check code style:**
   ```bash
   # Run linter (if available)
   python3 -m pylint app.py
   ```

### Create Pull Request

1. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub:**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Set base to `main` branch
   - Fill out the PR template

### PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues

Closes #(issue number)

## Testing Done

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No new warnings generated
```

### Review Process

1. **Automated checks** will run (linting, tests)
2. **Maintainers** will review your changes
3. **Address feedback** if requested
4. **Approval** from at least one maintainer required
5. **Merge** by a maintainer

---

## Coding Standards

### Python Code Style

Follow PEP 8:

```python
# Good
def calculate_disruption_tier(ticket_price, loyalty_status):
    """Calculate passenger tier based on ticket price."""
    if ticket_price > 1000 and loyalty_status == "premium":
        return "Gold"
    elif ticket_price > 500:
        return "Silver"
    return "Bronze"

# Bad
def calc_tier(tp,ls):
    if tp>1000 and ls=="premium":return "Gold"
    elif tp>500:return "Silver"
    return "Bronze"
```

### Naming Conventions

- **Variables:** `snake_case`
  ```python
  total_disrupted_passengers = 150
  disruption_duration_hours = 2.5
  ```

- **Functions:** `snake_case`
  ```python
  def get_eligible_passengers():
      pass
  
  def calculate_voucher_amount():
      pass
  ```

- **Classes:** `PascalCase`
  ```python
  class DisruptionDetector:
      pass
  
  class RecommendationEngine:
      pass
  ```

- **Constants:** `UPPER_SNAKE_CASE`
  ```python
  MAX_DELAY_HOURS = 24
  GOLD_TIER_MIN_PRICE = 1000
  ```

### Documentation

Add docstrings to all functions:

```python
def get_passenger_recommendations(passenger_id, disruption_id):
    """
    Generate AI-powered recommendations for a disrupted passenger.
    
    Args:
        passenger_id (str): Unique passenger identifier
        disruption_id (str): Unique disruption identifier
    
    Returns:
        dict: Recommendation with actions and priority
        {
            'recommendation_id': 'R001',
            'recommendation': 'Rebook on next flight...',
            'actions': ['premium_rebook', 'hotel'],
            'priority': 'high'
        }
    
    Raises:
        ValueError: If passenger_id or disruption_id is invalid
        Exception: If Ollama service is unavailable
    
    Example:
        >>> rec = get_passenger_recommendations('P001', 'D001')
        >>> print(rec['priority'])
        'high'
    """
```

### Comment Guidelines

```python
# Bad - obvious comment
x = 5  # Set x to 5

# Good - explains why
if ticket_price > 1000:
    # Premium passengers get Gold tier for priority handling
    tier = "Gold"
```

---

## Testing Guidelines

### Unit Tests

Create tests for new functions:

```python
# tests/test_recommendation_engine.py
import unittest
from recommendation_engine import get_passenger_recommendations

class TestRecommendationEngine(unittest.TestCase):
    
    def test_gold_tier_recommendation(self):
        """Test that high-value passengers get premium recommendations."""
        rec = get_passenger_recommendations('P001', 'D001')
        self.assertEqual(rec['tier'], 'Gold')
        self.assertIn('premium_rebook', rec['actions'])
    
    def test_invalid_passenger_id(self):
        """Test that invalid passenger ID raises ValueError."""
        with self.assertRaises(ValueError):
            get_passenger_recommendations('INVALID', 'D001')
```

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_recommendation_engine.py -v

# Run with coverage
python3 -m pytest tests/ --cov=. --cov-report=html

# Run specific test
python3 -m pytest tests/test_recommendation_engine.py::TestRecommendationEngine::test_gold_tier_recommendation -v
```

### Test Coverage

Aim for:
- **Core logic:** 80%+ coverage
- **Critical paths:** 100% coverage
- **Edge cases:** Comprehensive testing

---

## Documentation

### Update Documentation

When adding features, update relevant docs:

- **README.md** - Major features
- **API_REFERENCE.md** - API changes
- **Code comments** - Implementation details
- **Docstrings** - Function documentation
- **CHANGELOG.md** - Version history

### Documentation Style

- Use clear, concise language
- Include examples and code snippets
- Keep formatting consistent
- Add links to related sections

### Example Documentation

```markdown
## Feature Name

Brief description of feature.

### Usage

```python
# Code example
result = function_name(parameter)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| name | str | Description |

### Returns

Returns description and type.

### Examples

- Example 1
- Example 2
```

---

## Issue Reporting

### Before Creating an Issue

- Search existing issues to avoid duplicates
- Check documentation and FAQs
- Verify the issue is reproducible

### Issue Template

```markdown
## Description

Clear description of the issue.

## Expected Behavior

What should happen.

## Actual Behavior

What actually happens.

## Steps to Reproduce

1. Step 1
2. Step 2
3. Step 3

## Environment

- Python version: 3.9+
- OS: macOS/Linux/Windows
- Flask version: 3.1.3

## Screenshots

If applicable, add screenshots.

## Logs

Include relevant error messages:
```
Error message here
```

## Possible Solution

If you have ideas for fixing it.
```

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `documentation` - Documentation improvements
- `question` - Questions or discussions
- `help-wanted` - Help needed
- `good-first-issue` - Good for new contributors

---

## Development Workflow Summary

```
1. Fork repository
   ↓
2. Create feature branch
   ↓
3. Make changes
   ↓
4. Test thoroughly
   ↓
5. Commit with clear messages
   ↓
6. Push to fork
   ↓
7. Create pull request
   ↓
8. Address feedback
   ↓
9. Merge to main
   ↓
10. Update changelog
```

---

## Getting Help

### Questions

- Check [Discussions](https://github.com/RahulGosavi94/hack-ai-thon/discussions)
- Review [Documentation](DOCUMENTATION_INDEX.md)
- Check [API Reference](API_REFERENCE.md)

### Issues

- [Report a bug](https://github.com/RahulGosavi94/hack-ai-thon/issues/new?template=bug_report.md)
- [Request a feature](https://github.com/RahulGosavi94/hack-ai-thon/issues/new?template=feature_request.md)

### Contact

Reach out via [GitHub Issues](https://github.com/RahulGosavi94/hack-ai-thon/issues)

---

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Additional Resources

- [Python PEP 8 Style Guide](https://pep8.org/)
- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

Thank you for contributing! 🙏

**Last Updated:** January 12, 2026
