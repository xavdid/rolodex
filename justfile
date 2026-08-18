set quiet
set no-exit-message
set lazy

_default:
  just --list

_test:
  uv run -- pytest --quiet

lint *args:
  uv run -- ruff check {{ args }}

format *args:
  uv run -- ruff format {{ args }}

typecheck:
  uv run -- pyright

dev *args:
  uv run -- rolodex {{ args }}

prepare: _test (lint "--fix") format typecheck

bump level: _test lint (format "--check") typecheck
  uv version --bump {{ level }}

package_version := `uv run rolodex --version`

[confirm("This will release the package as written. Have you already run `just bump LEVEL`? (yN)")]
release:
  rm -rf dist
  uv build
  uv publish
  # gh release create v{{ package_version }} --notes "See [the changelog](https://github.com/xavdid/rolodex/blob/main/CHANGELOG.md#{{ replace(package_version, ".", "") }}) for detailed information."
