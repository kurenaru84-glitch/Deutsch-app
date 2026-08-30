#!/usr/bin/env python3
"""Extract German example sentences from Anki 定型表現365 .txt export."""
import csv
import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract_hints(html: str):
    hints = re.findall(r'display:\s*none">([^<]+)</div>', html, re.I)
    return [unescape(h.strip()) for h in hints if h.strip()]


def extract(src: Path):
    rows = []
    with src.open(encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) < 2 or row[0].startswith('#'):
                continue
            front_hints = extract_hints(row[0])
            back_hints = extract_hints(row[1])
            if front_hints and back_hints:
                rows.append({'de': front_hints[0], 'jp': back_hints[0]})
    return rows


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path.home() / 'Downloads' / 'ドイツ語定型表現365.txt'
    )
    rows = extract(src)
    data_dir = ROOT / 'data'
    data_dir.mkdir(exist_ok=True)

    with (data_dir / 'german-expression-examples.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ドイツ語例文', '日本語訳'])
        writer.writerows((row['de'], row['jp']) for row in rows)

    with (data_dir / 'german-expression-examples.tsv').open('w', encoding='utf-8', newline='') as f:
        f.write('ドイツ語例文\t日本語訳\n')
        for row in rows:
            de = row['de'].replace('\t', ' ').replace('\n', ' ')
            jp = row['jp'].replace('\t', ' ').replace('\n', ' ')
            f.write(f'{de}\t{jp}\n')

    js_lines = ['window.GERMAN_EXPRESSION_EXAMPLE_WORDS = [']
    for row in rows:
        js_lines.append(
            f'  {{de:{json.dumps(row["de"], ensure_ascii=False)}, jp:{json.dumps(row["jp"], ensure_ascii=False)}}},'
        )
    js_lines.append('];')
    js_lines.append('')
    (ROOT / 'words-german-expression-examples.js').write_text('\n'.join(js_lines), encoding='utf-8')
    print(f'Extracted {len(rows)} example sentences')


if __name__ == '__main__':
    main()
