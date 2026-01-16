# Contributing to AI News Intelligence Platform

Welcome! We're excited you want to contribute. This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Be respectful, inclusive, and professional. Treat all contributors with courtesy and respect.

## Getting Started

### 1. Fork the Repository
Click the "Fork" button on GitHub to create your own copy.

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/AI-Powered-News.git
cd AI-Powered-News
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install -e .

# Run with auto-reload
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

### Database Setup

```bash
docker-compose -f deployment/docker/docker-compose.yml up -d postgres redis
```

## Coding Standards

### Python
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints
- Write docstrings for all functions
- Use `black` for formatting

```bash
pip install black flake8
black app/
flake8 app/
```

### TypeScript/JavaScript
- Use `prettier` for formatting
- Use `eslint` for linting
- Use meaningful variable names

```bash
npm install prettier eslint
npx prettier --write src/
npx eslint src/
```

## Writing Tests

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

**Example test:**
```python
# backend/tests/test_api.py
def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Frontend Tests
```bash
cd frontend
npm test -- --coverage
```

## Commit Guidelines

Write clear, descriptive commit messages:

```bash
# Good
git commit -m "feat: add sentiment analysis endpoint"
git commit -m "fix: handle missing article images"
git commit -m "docs: update installation instructions"

# Avoid
git commit -m "update stuff"
git commit -m "wtf"
```

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Build, CI/CD, dependencies

## Pull Request Process

1. **Ensure tests pass**
   ```bash
   pytest tests/
   npm test
   ```

2. **Update documentation** if needed
   - Update README.md if behavior changes
   - Add docstrings to new functions
   - Update ARCHITECTURE.md for structural changes

3. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open a Pull Request**
   - Clear title and description
   - Reference any related issues: "Fixes #123"
   - Include screenshots for UI changes
   - Explain the reasoning behind changes

5. **Address review feedback**
   - Make requested changes
   - Push updates to same branch
   - Mark conversations as resolved

## Testing Checklist

Before submitting:
- [ ] Code follows style guidelines
- [ ] New tests added for new features
- [ ] All tests pass locally
- [ ] Documentation is updated
- [ ] No hardcoded credentials or secrets
- [ ] Commits are descriptive

## Areas for Contribution

### High Priority
- [ ] Mobile app UI improvements
- [ ] Performance optimizations
- [ ] Security hardening
- [ ] Test coverage expansion
- [ ] Documentation improvements

### Medium Priority
- [ ] New news sources integration
- [ ] Additional language support
- [ ] Advanced search features
- [ ] Export functionality
- [ ] Analytics dashboard

### Nice to Have
- [ ] Browser extension
- [ ] CLI tool
- [ ] Terraform deployment
- [ ] Monitoring dashboard
- [ ] API client libraries

## Reporting Issues

When reporting bugs:

1. **Check if issue already exists**
   Search closed and open issues

2. **Provide details**
   - OS and Python/Node version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and logs

3. **Include minimal example**
   Provide code that reproduces the issue

## Feature Requests

For feature requests:
1. Describe the use case
2. Explain the benefit
3. Provide examples if possible
4. Note any related features

## Documentation Contributions

- Update markdown files in repository root
- Follow existing style and structure
- Include code examples where appropriate
- Proofread for clarity

## Performance Considerations

When contributing:
- Profile code for bottlenecks
- Consider database query optimization
- Test with realistic data volumes
- Document performance characteristics

## Security

- Never commit `.env` files or credentials
- Report security issues privately
- Use environment variables for secrets
- Follow OWASP guidelines
- Update dependencies regularly

## Support

- 💬 Discussions: Use GitHub Discussions for questions
- 🐛 Issues: Report bugs on GitHub Issues
- 📖 Docs: Check ARCHITECTURE.md and QUICK_REFERENCE.md
- 📧 Email: Contact project maintainers

---

**Thank you for contributing! 🎉**

Your contributions help make this project better for everyone.
