set quiet

_default:
  just --list

lint:
  uv run ruff check src

lint-fix:
  uv run ruff check src --fix

format:
  uv run ruff format src

dev *args:
  uv run -- rolodex {{ args }}
