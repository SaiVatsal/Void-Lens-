# Contributing

## Setup

```bash
git clone https://github.com/voidlens/voidlens.git
cd voidlens
pip install -e ".[all]"
```

## Development Workflow

1. Create a feature branch
2. Make your changes
3. Run the test suite:

```bash
ruff check voidlens/ tests/
black voidlens/ tests/
mypy voidlens/
pytest tests/ -v --cov=voidlens
```

4. Submit a pull request

## Adding a New Module

See [PluginGuide.md](PluginGuide.md) for step-by-step instructions.

## Code Standards

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Add tests for new modules
- Keep modules independent — no cross-module imports

## Reporting Issues

Open an issue on GitHub with:
- VoidLens version (`voidlens version`)
- Python version
- OS
- Steps to reproduce
- Expected vs actual behavior
