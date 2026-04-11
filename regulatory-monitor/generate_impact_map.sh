#!/usr/bin/env bash
# generate_impact_map.sh — Scan DC-LEARN content for module references
# Usage: ./generate_impact_map.sh [module_id]
# If module_id is provided, only show files referencing that module.
# Otherwise, show all module references across the repo.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCES_FILE="$(dirname "$0")/sources.json"

# All 16 DC-LEARN modules (000–015)
MODULES=(000 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015)

if [[ $# -ge 1 ]]; then
    MODULES=("$1")
fi

echo "DC-LEARN Impact Map"
echo "==================="
echo "Scanning: $REPO_ROOT"
echo "Date: $(date -u +%Y-%m-%d)"
echo ""

for mod in "${MODULES[@]}"; do
    echo "--- Module $mod ---"
    # Search for module references in content files (md, html, json, yml)
    grep -rn --include="*.md" --include="*.html" --include="*.json" --include="*.yml" \
        -e "module.*${mod}" -e "Module.*${mod}" -e "\"${mod}\"" \
        "$REPO_ROOT" 2>/dev/null | grep -v "node_modules" | grep -v "regulatory-monitor/sources.json" || echo "  (no references found)"
    echo ""
done
