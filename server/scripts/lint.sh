#!/usr/bin/env bash

set -e
set -x

mypy src --check-untyped-defs  # type check
ruff check src tests        # linter
ruff format src --check # formatter
