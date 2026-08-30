#!/usr/bin/env python3
"""Extract phrase pairs from Anki TOEIC 金のフレーズ .txt export."""
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


def paren_phrase(line: str):
    line = line.strip()
    match = re.match(r'^[（(](.+)[）)]$', line)
    return match.group(1).strip() if match else None


def extract(src: Path):
    rows = []
    with src.open(encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) < 2 or row[0].startswith('#'):
                continue
            if 'font-family' not in row[0]:
                continue
            en_lines = [
                line.strip() for line in strip_html(row[0]).split('\n')
                if line.strip() and not line.startswith('[sound')
            ]
            jp_lines = [line.strip() for line in strip_html(row[1]).split('\n') if line.strip()]
            en_phrase = next((paren_phrase(line) for line in en_lines if paren_phrase(line)), None)
            jp_phrase = next((paren_phrase(line) for line in jp_lines if paren_phrase(line)), None)
            if en_phrase and jp_phrase:
                rows.append({'de': en_phrase, 'jp': jp_phrase})
    return rows


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path.home() / 'Downloads' / 'TOEIC L＆R TEST 出る単特急　金のフレーズ.txt'
    )
    rows = extract(src)
    data_dir = ROOT / 'data'
    data_dir.mkdir(exist_ok=True)

    with (data_dir / 'toeic-phrases.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['英語フレーズ', '日本語'])
        writer.writerows((row['de'], row['jp']) for row in rows)

    with (data_dir / 'toeic-phrases.tsv').open('w', encoding='utf-8', newline='') as f:
        f.write('英語フレーズ\t日本語\n')
        for row in rows:
            de = row['de'].replace('\t', ' ').replace('\n', ' ')
            jp = row['jp'].replace('\t', ' ').replace('\n', ' ')
            f.write(f'{de}\t{jp}\n')

    js_lines = ['window.TOEIC_PHRASE_WORDS = [']
    for row in rows:
        js_lines.append(f'  {{de:{json.dumps(row["de"], ensure_ascii=False)}, jp:{json.dumps(row["jp"], ensure_ascii=False)}}},')
    js_lines.append('];')
    js_lines.append('')
    (ROOT / 'words-toeic-phrases.js').write_text('\n'.join(js_lines), encoding='utf-8')
    print(f'Extracted {len(rows)} phrases')


if __name__ == '__main__':
    main()
