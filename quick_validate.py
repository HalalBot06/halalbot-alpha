import json
from pathlib import Path

bad = {}

for file in Path(".").glob("*.jsonl"):
    with open(file) as f:
        bad_lines = [i for i, line in enumerate(f, 1) if "text" not in json.loads(line)]
        if bad_lines:
            bad[file.name] = bad_lines

for filename, lines in bad.items():
    print(f"❌ {filename} has {len(lines)} invalid entries")
