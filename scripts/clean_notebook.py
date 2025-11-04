#!/usr/bin/env python3
"""
Clean notebook outputs and execution metadata.

This script removes:
1. Cell outputs
2. Execution counts
3. Execution metadata (timestamps)

This ensures notebooks are clean for version control while preserving
the original notebook metadata (language_info, etc).
"""

import json
import sys
from pathlib import Path
import subprocess


def clean_notebook(notebook_path: Path) -> None:
    """Clean a single notebook file while preserving original metadata."""
    # Get the original notebook metadata from git
    try:
        result = subprocess.run(
            ['git', 'show', f'HEAD:{notebook_path}'],
            capture_output=True,
            text=True,
            check=True
        )
        original_nb = json.loads(result.stdout)
        original_metadata = original_nb.get('metadata', {})
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        # If can't get from git, just use current metadata
        original_metadata = None

    # Load current notebook
    with open(notebook_path, 'r') as f:
        nb = json.load(f)

    # Preserve original metadata if we have it
    if original_metadata:
        nb['metadata'] = original_metadata

    # Clean each cell
    for cell in nb.get('cells', []):
        if cell['cell_type'] == 'code':
            # Clear outputs
            cell['outputs'] = []

            # Clear execution count
            cell['execution_count'] = None

            # Remove execution metadata (timestamps)
            if 'metadata' in cell and 'execution' in cell['metadata']:
                del cell['metadata']['execution']

    # Write back with consistent formatting
    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)
        f.write('\n')  # Add final newline


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: clean_notebook.py <notebook1.ipynb> [notebook2.ipynb ...]")
        sys.exit(1)

    for notebook_path in sys.argv[1:]:
        path = Path(notebook_path)
        if not path.exists():
            print(f"Error: {path} does not exist", file=sys.stderr)
            sys.exit(1)

        clean_notebook(path)
        print(f"Cleaned: {path}")


if __name__ == '__main__':
    main()
