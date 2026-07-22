#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/build_diagrams.sh"
"$SCRIPT_DIR/build_guide.sh" all
python3 "$SCRIPT_DIR/validate_routes.py"
python3 "$SCRIPT_DIR/validate_continuity.py"
python3 "$SCRIPT_DIR/validate_guide.py"
python3 "$SCRIPT_DIR/verify_layout.py"
python3 "$SCRIPT_DIR/verify_density.py"
python3 "$SCRIPT_DIR/verify_accessibility.py"
node "$SCRIPT_DIR/verify_overflow.mjs"
