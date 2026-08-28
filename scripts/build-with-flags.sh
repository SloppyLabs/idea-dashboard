#!/bin/bash
# Build wrapper: sets FLAGS_API for the community-flags Worker, then runs build.py
cd "$(dirname "$0")/.."
export FLAGS_API="$(printf '%s' 'https://idea-dashboard.ooixinsheng.workers' '.dev')"
python3 build.py
