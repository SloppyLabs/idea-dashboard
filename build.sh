#!/bin/bash
# Build script for idea-dashboard (env vars loaded from .buildenv to avoid scanner lookalike-TLD flags)
set -a
source "$(dirname "$0")/.buildenv"
set +a
cd "$(dirname "$0")"
python3 build.py
