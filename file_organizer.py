"""
file_organizer.py – Organize files in a directory by their extension.
Usage: python file_organizer.py <target_directory>
"""
import os
import shutil
import sys

CATEGORY_MAP = {
    'Images':    ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.csv'],
    'Videos':    ['.mp4', '.mkv', '.avi', '.mov', '.wmv'],
    'Audio':     ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    'Archives':  ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Code':      ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp'],
}


def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return 'Others'


def organize(target_dir: str, dry_run: bool = False) -> dict:
    """Move files into categorized sub-folders. Returns move counts."""
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    counts = {}
    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1]
            category = get_category(ext)
            dest_dir = os.path.join(target_dir, category)

            if not dry_run:
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(filepath, os.path.join(dest_dir, filename))

            counts[category] = counts.get(category, 0) + 1

    return counts


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python file_organizer.py <directory>")
        sys.exit(1)

    target = sys.argv[1]
    dry = '--dry-run' in sys.argv
    result = organize(target, dry_run=dry)

    print(f"\n{'[DRY RUN] ' if dry else ''}Organized files:")
    for cat, count in sorted(result.items()):
        print(f"  {cat}: {count} file(s)")
    print(f"\nTotal: {sum(result.values())} files processed.")
