"""
file_organizer.py – Organize files in a directory by their extension.
Usage: python file_organizer.py <target_directory> [--dry-run] [--undo]
"""
import os
import sys
import json
import shutil
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

CATEGORY_MAP = {
    'Images':    ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.csv', '.md'],
    'Videos':    ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv'],
    'Audio':     ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
    'Archives':  ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'Code':      ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp', '.ts'],
}

MANIFEST_FILE = '.organize_manifest.json'


def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return 'Others'


def organize(target_dir: str, dry_run: bool = False) -> dict:
    """Move files into categorized sub-folders. Returns move counts."""
    if not os.path.isdir(target_dir):
        logger.error(f"'{target_dir}' is not a valid directory.")
        sys.exit(1)

    counts = {}
    manifest = []

    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)

        # Skip directories, hidden files, and the manifest
        if not os.path.isfile(filepath) or filename.startswith('.'):
            continue

        ext = os.path.splitext(filename)[1]
        category = get_category(ext)
        dest_dir = os.path.join(target_dir, category)
        dest_path = os.path.join(dest_dir, filename)

        if not dry_run:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(filepath, dest_path)
            manifest.append({'src': filepath, 'dest': dest_path})
            logger.info(f"Moved: {filename} → {category}/")
        else:
            logger.info(f"[DRY RUN] Would move: {filename} → {category}/")

        counts[category] = counts.get(category, 0) + 1

    # Save manifest for undo support
    if not dry_run and manifest:
        manifest_path = os.path.join(target_dir, MANIFEST_FILE)
        with open(manifest_path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'moves': manifest,
            }, f, indent=2)

    return counts


def undo(target_dir: str):
    """Undo the last organize operation using the manifest."""
    manifest_path = os.path.join(target_dir, MANIFEST_FILE)
    if not os.path.exists(manifest_path):
        logger.error("No manifest found. Nothing to undo.")
        return

    with open(manifest_path) as f:
        data = json.load(f)

    for move in reversed(data['moves']):
        if os.path.exists(move['dest']):
            shutil.move(move['dest'], move['src'])
            logger.info(f"Restored: {os.path.basename(move['src'])}")

    os.remove(manifest_path)
    logger.info("Undo complete.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python file_organizer.py <directory> [--dry-run] [--undo]")
        sys.exit(1)

    target = sys.argv[1]

    if '--undo' in sys.argv:
        undo(target)
    else:
        dry = '--dry-run' in sys.argv
        result = organize(target, dry_run=dry)

        print(f"\n{'[DRY RUN] ' if dry else ''}Organized files:")
        for cat, count in sorted(result.items()):
            print(f"  {cat}: {count} file(s)")
        print(f"  Total: {sum(result.values())} files processed.")
