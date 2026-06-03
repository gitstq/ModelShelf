.PHONY: install install-dev test test-cov lint format clean build publish docs

# Default Python interpreter
PYTHON := python3
PIP := $(PYTHON) -m pip

# Install dependencies
install:
	$(PIP) install -e .

# Install development dependencies
install-dev:
	$(PIP) install -e ".[dev]"

# Run tests
test:
	$(PYTHON) -m pytest tests/ -v

# Run tests with coverage
test-cov:
	$(PYTHON) -m pytest tests/ -v --cov=modelshelf --cov-report=html --cov-report=term

# Lint code
lint:
	ruff check modelshelf/ tests/
	mypy modelshelf/

# Format code
format:
	black modelshelf/ tests/
	ruff check --fix modelshelf/ tests/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build package
build: clean
	$(PYTHON) -m build

# Publish to PyPI (requires credentials)
publish: build
	$(PYTHON) -m twine upload dist/*

# Generate documentation
docs:
	cd docs && make html

# Run CLI
run:
	$(PYTHON) -m modelshelf

# Interactive TUI
tui:
	$(PYTHON) -c "from modelshelf.tui import run_tui; import asyncio; asyncio.run(run_tui())"

# Development server (for testing)
dev:
	$(PYTHON) -m modelshelf status
