"""
csv_analyzer.py – Quick stats and summary for CSV files.
Usage: python csv_analyzer.py <file.csv>
"""
import csv
import sys
from collections import defaultdict


def analyze(filepath: str):
    """Print basic stats for a CSV file."""
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("CSV is empty.")
        return

    headers = list(rows[0].keys())
    print(f"File   : {filepath}")
    print(f"Rows   : {len(rows)}")
    print(f"Columns: {len(headers)}")
    print(f"Headers: {', '.join(headers)}")

    print("\n--- Column Summary ---")
    for col in headers:
        values = [r[col] for r in rows if r[col]]
        unique = len(set(values))
        empty  = sum(1 for r in rows if not r[col])
        print(f"  {col}: {unique} unique, {empty} empty")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python csv_analyzer.py <file.csv>")
        sys.exit(1)
    analyze(sys.argv[1])
