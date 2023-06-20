#!/bin/bash
set -Eeuo pipefail

isort openhxai/ tests/
black openhxai/ tests/
make run-checks
