#!/usr/bin/env python3
"""Extract JP/EN sentences from Anki DUO Select .txt export."""
import csv
import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def strip_html(html: str) -> str:
    text = re.sub(r'<br\s*/?>', '\n', html, flags=re.I)
    text = re.sub(r'<[^>]+>', '', text)
    return unescape(text.replace('""', '"')).strip()


def clean_side(raw: str) -> str:
    lines = [line.strip() for line in strip_html(raw).split('\n') if line.strip()]
    kept = []
    for line in lines:
        if line.startswith('DUOSELECT_'):
            continue
        if re.match(r'SECTION\d+\s+例文\d+', line):
            continue
        if line.startswith('[sound:'):
            continue
        kept.append(line)
    return '\n'.join(kept).strip()


def auto_chunks(en: str):
    if '\n' in en:
        lines = [line.strip() for line in en.split('\n') if line.strip()]
        if len(lines) >= 2:
            return lines
    parts = [p.strip() for p in re.split(r'(?<=[.!?])\s+', en) if p.strip()]
    if len(parts) >= 2:
        return parts
    parts = [p.strip() for p in en.split(',') if p.strip()]
    if len(parts) >= 2:
        return parts
    words = en.split()
    if len(words) >= 6:
        mid = len(words) // 2
        return [' '.join(words[:mid]), ' '.join(words[mid:])]
    if len(words) >= 3:
        return [' '.join(words[:2]), ' '.join(words[2:])]
    return None


def extract(src: Path):
    rows = []
    with src.open(encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) < 2 or row[0].startswith('#'):
                continue
            if 'DUOSELECT' not in row[0]:
                continue
            en = clean_side(row[0])
            jp = clean_side(row[1])
            chunks = auto_chunks(en)
            if en and jp and chunks:
                rows.append({'jp': jp, 'en': en, 'chunks': chunks})
    return rows


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / 'Downloads' / 'DUO Select.txt'
    rows = extract(src)
    data_dir = ROOT / 'data'
    data_dir.mkdir(exist_ok=True)

    with (data_dir / 'duo-select-sentences.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['日本語', '英語'])
        w.writerows((r['jp'], r['en']) for r in rows)

    with (data_dir / 'duo-select-sentences.tsv').open('w', encoding='utf-8', newline='') as f:
        f.write('日本語\t英語\n')
        for r in rows:
            jp = r['jp'].replace('\t', ' ').replace('\n', ' / ')
            en = r['en'].replace('\t', ' ').replace('\n', ' / ')
            f.write(f'{jp}\t{en}\n')

    with (data_dir / 'duo-select-sentences-app.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['日本語', '英語（| または / でチャンク区切り）'])
        for r in rows:
            w.writerow([r['jp'], ' / '.join(r['chunks'])])

    js_lines = ['window.DUO_SELECT_SENTENCES = [']
    for r in rows:
        js_lines.append('    {')
        js_lines.append(f'        jp: {json.dumps(r["jp"], ensure_ascii=False)},')
        chunks_js = ', '.join(json.dumps(c, ensure_ascii=False) for c in r['chunks'])
        js_lines.append(f'        chunks: [{chunks_js}]')
        js_lines.append('    },')
    js_lines.append('];')
    js_lines.append('')
    (ROOT / 'sentences-duo-select.js').write_text('\n'.join(js_lines), encoding='utf-8')
    print(f'Extracted {len(rows)} sentences')


if __name__ == '__main__':
    main()
