"""
json_formatter.py – Pretty-print and validate JSON files.
Usage: python json_formatter.py <file.json> [--indent N] [--sort-keys]
"""
import json
import sys
import argparse


def format_json(filepath: str, indent: int = 2, sort_keys: bool = False) -> str:
    """Read, validate, and pretty-print a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='JSON formatter & validator')
    parser.add_argument('file', help='Path to JSON file')
    parser.add_argument('--indent', type=int, default=2, help='Indentation level')
    parser.add_argument('--sort-keys', action='store_true', help='Sort object keys')
    parser.add_argument('--write', action='store_true', help='Write formatted output back')
    args = parser.parse_args()

    formatted = format_json(args.file, indent=args.indent, sort_keys=args.sort_keys)

    if args.write:
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(formatted + '\n')
        print(f"Formatted and saved: {args.file}")
    else:
        print(formatted)


if __name__ == '__main__':
    main()
