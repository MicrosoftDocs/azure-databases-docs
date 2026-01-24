#!/usr/bin/env python3
"""Add ms.subservice metadata to remaining PostgreSQL documentation folders."""

import os
import re
from pathlib import Path

# Base path for PostgreSQL docs
BASE_PATH = Path(r"c:\GitHub\repos\azure-databases-docs-pr\articles\postgresql")

# Folder to subservice mapping for remaining folders (except server-parameters)
FOLDER_MAPPINGS = {
    "monitor": "monitoring",
    "troubleshoot": "performance",
    "extensions": "extensions",
    "security": "security",
    "configure-maintain": "configuration",
    "migrate": "migration",
}

def add_subservice_to_file(file_path: Path, subservice: str) -> tuple[bool, str]:
    """Add ms.subservice after ms.service in the file's YAML frontmatter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if ms.subservice already exists
        if 'ms.subservice:' in content:
            return False, "Already has ms.subservice"
        
        # Find ms.service line and add ms.subservice after it
        # Pattern matches ms.service: followed by any value
        pattern = r'(ms\.service:\s*[^\n]+\n)'
        replacement = f'\\1ms.subservice: {subservice}\n'
        
        new_content, count = re.subn(pattern, replacement, content, count=1)
        
        if count == 0:
            return False, "Could not find ms.service line"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"Added ms.subservice: {subservice}"
    
    except Exception as e:
        return False, f"Error: {str(e)}"

def process_folder(folder_name: str, subservice: str) -> tuple[int, int]:
    """Process all markdown files in a folder."""
    folder_path = BASE_PATH / folder_name
    
    if not folder_path.exists():
        print(f"  ⚠️  Folder not found: {folder_path}")
        return 0, 0
    
    md_files = list(folder_path.glob("*.md"))
    print(f"Found {len(md_files)} markdown files")
    
    modified = 0
    skipped = 0
    
    for md_file in sorted(md_files):
        success, message = add_subservice_to_file(md_file, subservice)
        if success:
            print(f"  ✅ {md_file.name}: {message}")
            modified += 1
        else:
            print(f"  ⏭️  {md_file.name}: {message}")
            skipped += 1
    
    return modified, skipped

def main():
    print("Adding ms.subservice to ALL remaining PostgreSQL documentation folders")
    print(f"Folders: {', '.join(FOLDER_MAPPINGS.keys())}")
    print()
    
    total_modified = 0
    total_skipped = 0
    
    for folder, subservice in FOLDER_MAPPINGS.items():
        print("=" * 60)
        print(f"Processing: {folder}/ → ms.subservice: {subservice}")
        print("=" * 60)
        
        modified, skipped = process_folder(folder, subservice)
        total_modified += modified
        total_skipped += skipped
        print()
    
    print("=" * 60)
    print(f"TOTAL: {total_modified} files modified, {total_skipped} files skipped")
    print("=" * 60)

if __name__ == "__main__":
    main()
