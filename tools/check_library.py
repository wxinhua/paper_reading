#!/usr/bin/env python3
"""Check the generated library's inventory, figure hashes and local links."""

import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = set()
        self.references = []
        self.entries = []
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                raise ValueError('Duplicate HTML ID: ' + attrs['id'])
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.references.append(attrs[key])
        if tag == 'article' and 'paper-entry' in attrs.get('class', '').split():
            self.entries.append(attrs)


def check():
    library = json.loads((ROOT / 'library.json').read_text())
    papers = library['papers']
    identifiers = [paper['id'] for paper in papers]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError('Duplicate paper IDs')
    if {ROOT / paper['note_path'] for paper in papers} != set((ROOT / 'papers').glob('*.md')):
        raise ValueError('Paper notes and registry differ')
    readers = [ROOT / paper['reader_path'] for paper in papers]
    readers += [ROOT / item['reader_path'] for item in library.get('reading_lists', [])]
    readers.append(ROOT / 'index.html')
    parsed = {path: Links(path.read_text()) for path in readers}
    if len(parsed[ROOT / 'index.html'].entries) != len(papers):
        raise ValueError('Index entry count differs from registry')
    checked = 0
    for path, document in parsed.items():
        for href in document.references:
            parts = urlsplit(href)
            if parts.scheme in ('http', 'https') or parts.netloc:
                continue
            if parts.scheme:
                raise ValueError('Nonportable URL: ' + href)
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if not target.is_relative_to(ROOT) or not target.exists():
                raise ValueError(f'Broken local link in {path.name}: {href}')
            if parts.fragment and target.suffix == '.html':
                if target not in parsed or unquote(parts.fragment) not in parsed[target].ids:
                    raise ValueError(f'Broken anchor in {path.name}: {href}')
            checked += 1
    figures = 0
    for path in (ROOT / 'assets').rglob('manifest.json'):
        manifest = json.loads(path.read_text())
        for figure in manifest.get('figures', []):
            image = path.parent / figure['file'] if figure.get('file') else ROOT / figure['path']
            if hashlib.sha256(image.read_bytes()).hexdigest() != figure['sha256']:
                raise ValueError('Figure checksum changed: ' + str(image))
            figures += 1
    result = {'papers': len(papers), 'reader_pages': len(readers), 'figures': figures,
              'local_links_checked': checked, 'broken_links': 0}
    print(json.dumps(result, ensure_ascii=False))
    return result


if __name__ == '__main__':
    check()
