#!/bin/bash
# Rebuild the idea dashboard with the community-flags API endpoint injected.
set -e
cd "$(dirname "$0")"
FLAGS_API="$(cat .flags_api_url)" python3 build.py
