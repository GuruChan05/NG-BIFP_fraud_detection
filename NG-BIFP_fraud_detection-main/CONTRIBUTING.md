# Contributing to NG-BIFP

## 🎯 How to Contribute

We welcome contributions from the community! Please follow these guidelines:

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR-USERNAME/NG-BIFP_fraud_detection.git
cd NG-BIFP_fraud_detection
git remote add upstream https://github.com/GuruChan05/NG-BIFP_fraud_detection.git
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
- Follow code style guidelines
- Write/update tests
- Update documentation

### 4. Commit with Conventional Commits
```bash
git commit -m "feat: add new fraud detection model"
```

Commit types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Dependencies

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## 📋 Code Standards

### Backend (Python)
```bash
# Format with Black
black app/

# Lint with flake8
flake8 app/

# Type checking with mypy
mypy app/
```

### Frontend (TypeScript/React)
```bash
# Format with Prettier
npm run format

# Lint with ESLint
npm run lint

# Type checking
npm run type-check
```

## 🧪 Testing Requirements

- Backend: Write tests for new features
- Frontend: Write tests for new components
- Run full test suite before submitting PR

```bash
# Backend
cd ngbfip/backend && pytest

# Frontend
cd ngbfip/frontend && npm test
```

## 📝 Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Related Issues
Closes #(issue number)

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🐛 Reporting Issues

### Bug Report
Include:
1. Description
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details
6. Screenshots/logs

### Feature Request
Include:
1. Use case
2. Proposed solution
3. Alternative solutions
4. Additional context

## 📚 Documentation

- Keep README.md updated
- Document new APIs
- Add code comments for complex logic
- Update CHANGELOG.md

## 🚀 Release Process

1. Update version in `package.json` and `setup.py`
2. Update CHANGELOG.md
3. Create release notes
4. Tag release: `git tag v1.0.0`
5. Push tags: `git push --tags`

## ❓ Questions?

Open a GitHub discussion or issue for questions.

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.
