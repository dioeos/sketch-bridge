#!/usr/bin/env bash
set -x

ruff check src scripts tests --fix
ruff format src scripts tests
