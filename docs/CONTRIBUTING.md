# Contributing to Gemma 3 270M Minimal Container

Thank you for your interest in contributing to this project!

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or suggest features
- Provide clear description and reproduction steps
- Include environment details (OS, Docker version, architecture)

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Keep functions focused and small

### Docker Best Practices

- Keep images minimal
- Use multi-stage builds
- Remove unnecessary packages
- Use non-root users
- Leverage layer caching

### Testing

Before submitting a PR:

```bash
# Validate Python sources
python -m compileall -q src/

# Verify expected project files
./scripts/verify-project.sh

# Build the fast-start image
./scripts/build-container-image.sh
```

### Performance Considerations

When optimizing:

1. Measure before and after
2. Consider both size and speed
3. Test on multiple architectures
4. Document trade-offs

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add tests for new features
4. Keep commits atomic and well-described
5. Link related issues

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open an issue or reach out to maintainers for guidance.
