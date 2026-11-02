#!/usr/bin/env bash
# Regenerate the clip shelves (run from repo root). Needs analysis/{flat,disk}_hmap.npz (made by analysis/hmap.py).
set -e
cd "$(dirname "$0")/../analysis"
G=../tools/shelf_groups.json
FLAT=$(python3 -c "import json;print(json.dumps(json.load(open('$G'))['flat']))")
DISK=$(python3 -c "import json;print(json.dumps(json.load(open('$G'))['disk']))")
python3 shelves.py flat ../sources/rhys34512-printables-973426/flat-panel-side.stl lo "$FLAT" > flat_report.json
python3 shelves.py disk ../sources/rhys34512-printables-973426/disk-panel.stl hi "$DISK" > disk_report.json
echo "shelves written to analysis/shelf_*.stl"
