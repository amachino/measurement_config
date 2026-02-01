.PHONY: sync test check fix

# Install dependencies
sync:
	uv sync --all-groups --all-extras

# Run unit tests
test:
	uv run pytest

# Run type, lint, and format checks
check:
	uv run pyright
	uv run ruff check
	uv run ruff format --check

# Auto-fix formatting and lint issues
fix:
	uv run ruff format
	uv run ruff check --fix

# Remove caches and build artifacts
clean:
	rm -rf dist build *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .mypy_cache
