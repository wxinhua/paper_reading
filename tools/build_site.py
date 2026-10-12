#!/usr/bin/env python3
"""Build the offline reader and the GitHub Pages artifact using Python only."""

import json
import shutil
from pathlib import Path

import build_reader
import check_library

ROOT = Path(__file__).resolve().parents[1]


def main():
    build_reader.main()
    result = check_library.check()
    destination = ROOT / 'dist'
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir()
    library = json.loads((ROOT / 'library.json').read_text())
    files = [ROOT / 'index.html', ROOT / 'library.json', ROOT / 'template.md']
    files += [ROOT / paper['reader_path'] for paper in library['papers']]
    files += [ROOT / item['reader_path'] for item in library.get('reading_lists', [])]
    for folder in ('papers', 'research', 'assets'):
        files += [path for path in (ROOT / folder).rglob('*') if path.is_file() and path.suffix in ('.md', '.png', '.json')]
    for path in files:
        target = destination / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    (destination / '.nojekyll').write_text('')
    print('Built deployable dist/ with ' + str(result['papers']) + ' papers.')


if __name__ == '__main__':
    main()

