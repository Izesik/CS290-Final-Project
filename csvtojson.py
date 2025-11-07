import pandas as pd
import sys
from pathlib import Path

def csv_to_json(csv_path, json_path=None):
    csv_path = Path(csv_path)
    if json_path is None:
        json_path = csv_path.with_suffix(".json")
    else:
        json_path = Path(json_path)

    df = pd.read_csv(csv_path, low_memory=False)
    df.to_json(json_path, orient="records", indent=2)
    print(f"Saved JSON to {json_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python csv_to_json.py <input.csv> [output.json]")
        sys.exit(1)

    csv_path = sys.argv[1]
    json_path = sys.argv[2] if len(sys.argv) > 2 else None
    csv_to_json(csv_path, json_path)
