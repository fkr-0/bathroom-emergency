#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/build_diagrams.sh"
python3 "$SCRIPT_DIR/build_inventories.py"
python3 "$SCRIPT_DIR/build_source_inventory.py"
"$SCRIPT_DIR/build_guide.sh" all
python3 "$SCRIPT_DIR/build_subguides.py" --node all
python3 "$SCRIPT_DIR/validate_routes.py"
python3 "$SCRIPT_DIR/validate_continuity.py"
python3 "$SCRIPT_DIR/validate_subguides.py"
python3 "$SCRIPT_DIR/validate_visualizations.py"
python3 "$SCRIPT_DIR/validate_migration.py"
python3 "$SCRIPT_DIR/validate_illustrations.py"
python3 "$SCRIPT_DIR/validate_guide.py"
python3 "$SCRIPT_DIR/verify_layout.py"
python3 "$SCRIPT_DIR/verify_density.py"
python3 "$SCRIPT_DIR/verify_accessibility.py"
node "$SCRIPT_DIR/verify_overflow.mjs"
