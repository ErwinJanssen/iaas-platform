# Contributing to IaaS Platform

We welcome contributions from the community! This document outlines how you can contribute to the IaaS Platform project.

## Ways to Contribute

- **Code Contributions**: Submit bug fixes, new features, or improvements
- **Documentation**: Improve or add documentation
- **Testing**: Report bugs or add test cases
- **Feature Requests**: Suggest new features or enhancements
- **Code Review**: Review pull requests from other contributors
- **Discussions**: Participate in discussions about the project

## Getting Started

### 1. Fork the Repository

Click the "Fork" button on the top-right of the [IaaS Platform repository](https://github.com/ErwinJanssen/iaas-platform) to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/iaas-platform.git
cd iaas-platform
```

### 3. Set Up Development Environment

Follow the instructions in [DEVELOPMENT.md](docs/DEVELOPMENT.md) to set up your local development environment.

### 4. Create a Branch

Create a feature branch for your changes:

```bash
# For a new feature
git checkout -b feature/your-feature-name

# For a bug fix
git checkout -b fix/your-bug-fix

# For documentation
git checkout -b docs/your-docs-update
```

### 5. Make Your Changes

Make your changes following the coding standards outlined in [DEVELOPMENT.md](docs/DEVELOPMENT.md).

### 6. Run Tests

Ensure all tests pass:

```bash
make test
```

### 7. Run Linters

Ensure your code follows the style guidelines:

```bash
make lint
```

### 8. Commit Your Changes

Follow the [Conventional Commits](https://www.conventionalcommits.org/) format for commit messages:

```bash
git add .
git commit -m "feat(api): add new VM endpoint"
```

### 9. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 10. Create a Pull Request

Go to the [IaaS Platform repository](https://github.com/ErwinJanssen/iaas-platform) and create a pull request from your branch to the `main` branch.

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass (`make test`)
- [ ] Code passes linting (`make lint`)
- [ ] Code is properly formatted (`make format`)
- [ ] Documentation is updated (if applicable)
- [ ] No secrets or sensitive information are committed
- [ ] Commit messages follow Conventional Commits format

### Pull Request Template

Use the following template for your pull request:

```markdown
## Description

[Brief description of changes]

## Related Issues

- Closes #123
- Related to #456

## Changes Made

- [ ] Feature implementation
- [ ] Bug fix
- [ ] Documentation update
- [ ] Test coverage
- [ ] Breaking changes (if any)

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Screenshots (if applicable)

## Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Code Review Process

1. **Initial Review**: A maintainer will review your PR within 24-48 hours
2. **Feedback**: You may receive feedback requesting changes
3. **Address Feedback**: Make requested changes and push to your branch
4. **Approval**: Once approved, a maintainer will merge your PR
5. **CI Checks**: All CI checks must pass before merging

## Reporting Bugs

### Before Reporting

- Check the [issue tracker](https://github.com/ErwinJanssen/iaas-platform/issues) for existing issues
- Ensure you're using the latest version
- Try to reproduce the issue in a clean environment

### Bug Report Template

Use the following template when creating a bug report:

```markdown
## Description

[Clear and concise description of the bug]

## Steps to Reproduce

1. [First step]
2. [Second step]
3. [Third step]

## Expected Behavior

[What you expected to happen]

## Actual Behavior

[What actually happened]

## Environment

- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11.4]
- IaaS Platform version: [e.g., 0.1.0]

## Additional Context

[Any additional context, logs, or screenshots]
```

## Requesting Features

### Before Requesting

- Check the [roadmap](docs/ROADMAP.md) for planned features
- Search existing feature requests

### Feature Request Template

Use the following template when requesting a feature:

```markdown
## Description

[Clear and concise description of the feature]

## Use Case

[Why this feature is needed and how it would be used]

## Proposed Solution

[Your ideas for implementing the feature]

## Alternatives Considered

[Any alternative solutions you've considered]

## Additional Context

[Any additional context or examples]
```

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). We expect all contributors to:

- Be respectful and inclusive
- Focus on constructive criticism
- Follow the project's coding standards
- Respect differing viewpoints

## Recognition

All contributors will be recognized in the project's contributors list. Significant contributions may receive additional recognition.

## License

By contributing to this project, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).

## Questions?

If you have any questions about contributing, please:

1. Check the [documentation](docs/)
2. Look at existing [issues](https://github.com/ErwinJanssen/iaas-platform/issues) and [pull requests](https://github.com/ErwinJanssen/iaas-platform/pulls)
3. Open a [discussion](https://github.com/ErwinJanssen/iaas-platform/discussions)
4. Contact the maintainers

Thank you for your contributions!
