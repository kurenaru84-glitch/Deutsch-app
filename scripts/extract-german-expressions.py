#!/usr/bin/env python3
"""Extract German fixed expressions from Anki 定型表現365 .txt export."""
import csv
import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def strip_html(html: str) -> str:
    text = re.sub(r'<br\s*/?>', '\n', html, flags=re.I)
    text = re.sub(r'<[^>]+>', '\n', text)
    return unescape(text.replace('""', '"'))


def normalize_placeholder(text: str) -> str:
    return text.replace('...4', '...').replace('  ', ' ').strip()


def extract_row(row0: str, row1: str):
    phrase_part = re.split(r'<hr\b', row0, flags=re.I)[0]
    de = normalize_placeholder(strip_html(phrase_part))
    jp_match = re.search(r'color:#53a8b6[^>]*>([^<]+)<', row1, re.I)
    jp = normalize_placeholder(jp_match.group(1).strip()) if jp_match else None
    return de, jp


def extract(src: Path):
    rows = []
    with src.open(encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) < 2 or row[0].startswith('#'):
                continue
            de, jp = extract_row(row[0], row[1])
            if de and jp:
                rows.append({'de': de, 'jp': jp})
    return rows


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path.home() / 'Downloads' / 'ドイツ語定型表現365.txt'
    )
    rows = extract(src)
    data_dir = ROOT / 'data'
    data_dir.mkdir(exist_ok=True)

    with (data_dir / 'german-expressions.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ドイツ語フレーズ', '日本語'])
        writer.writerows((row['de'], row['jp']) for row in rows)

    with (data_dir / 'german-expressions.tsv').open('w', encoding='utf-8', newline='') as f:
        f.write('ドイツ語フレーズ\t日本語\n')
        for row in rows:
            de = row['de'].replace('\t', ' ').replace('\n', ' ')
            jp = row['jp'].replace('\t', ' ').replace('\n', ' ')
            f.write(f'{de}\t{jp}\n')

    js_lines = ['window.GERMAN_EXPRESSION_WORDS = [']
    for row in rows:
        js_lines.append(
            f'  {{de:{json.dumps(row["de"], ensure_ascii=False)}, jp:{json.dumps(row["jp"], ensure_ascii=False)}}},'
        )
    js_lines.append('];')
    js_lines.append('')
    (ROOT / 'words-german-expressions.js').write_text('\n'.join(js_lines), encoding='utf-8')
    print(f'Extracted {len(rows)} expressions')


if __name__ == '__main__':
    main()
