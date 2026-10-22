# -*- coding: utf-8 -*-
"""Trích dữ liệu Speaking Part 1 & 2 từ hai file .docx sang dữ liệu cho công cụ.

Chạy:  python import-speaking.py
Sinh ra:
  data/part1.js        21 câu hỏi Part 1 kèm chiến lược, mẫu trả lời, từ vựng
  data/part2.js        17 bộ Part 2 kèm 3 nhiệm vụ, phần trả lời để trống
  media/part2/NN.jpg   ảnh đã nén cho Part 2
"""
import io, json, os, re, zipfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'Input doc', 'Speaking')
P1_DOC = os.path.join(SRC, 'M- Aptis_Speaking_Part_1_Chuan_B2_Updated.docx')
P2_DOC = os.path.join(SRC, 'VMEC_Speaking Aptis - Part 1-2 (apdate 08.10).docx')
DATA = os.path.join(HERE, 'data')
MEDIA = os.path.join(HERE, 'media', 'part2')

TAG = re.compile(r'<[^>]+>')


def xml_of(path, name='word/document.xml'):
    with zipfile.ZipFile(path) as z:
        return z.read(name).decode('utf-8')


def text_of(frag):
    s = frag.replace('<w:tab/>', '\t')
    s = re.sub(r'<w:br[^>]*/>', '\n', s)
    s = s.replace('</w:p>', '\n')
    s = TAG.sub('', s)
    for a, b in (('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")):
        s = s.replace(a, b)
    s = re.sub(r'[ \t]+', ' ', s)
    return '\n'.join(ln.strip() for ln in s.split('\n') if ln.strip())


# ---------- Part 1 ----------
VOCAB_LINE = re.compile(
    r'^[•\-\*\s]*(?P<w>[A-Za-z][A-Za-z\'\- ]*?)\s*/(?P<ipa>[^/]+)/\s*(?:\((?P<pos>[^)]*)\))?\s*[:：]\s*(?P<vi>.+)$')


def parse_part1():
    xml = xml_of(P1_DOC)
    tbl = re.search(r'<w:tbl>[\s\S]*?</w:tbl>', xml).group(0)
    rows = re.findall(r'<w:tr\b[\s\S]*?</w:tr>', tbl)
    out = []
    for r in rows[1:]:                      # bỏ hàng tiêu đề
        cells = [text_of(c) for c in re.findall(r'<w:tc>[\s\S]*?</w:tc>', r)]
        if len(cells) < 4:
            continue
        group = ' '.join(cells[0].split('\n')).replace('Nhóm ', 'Nhóm ').strip()
        q = re.sub(r'^\d+\.\s*', '', cells[1].replace('\n', ' ')).strip()
        strategy = cells[2].replace('\n', ' ').strip()
        raw_ans = cells[3].replace('\n', ' ').strip()
        # một số ô chứa hai phiên bản trả lời, ngăn bằng -- hoặc ---
        parts = [p.strip(' "“”\'').strip() for p in re.split(r'\s-{2,}\s*', raw_ans) if p.strip(' "“”\'').strip()]
        answer = parts[0] if parts else ''
        alt = parts[1] if len(parts) > 1 else ''
        vocab = []
        if len(cells) > 4:
            for ln in cells[4].split('\n'):
                m = VOCAB_LINE.match(ln.strip())
                if m:
                    vocab.append({'w': m.group('w').strip().lower(),
                                  'ipa': '/' + m.group('ipa').strip() + '/',
                                  'pos': (m.group('pos') or '').strip(),
                                  'vi': m.group('vi').strip().rstrip('.')})
        if q and answer:
            out.append({'id': 'p1-%02d' % (len(out) + 1), 'group': group,
                        'q': q, 'strategy': strategy, 'answer': answer, 'alt': alt, 'vocab': vocab})
    return out


# ---------- Part 2 ----------
def parse_part2():
    xml = xml_of(P2_DOC)
    rels = xml_of(P2_DOC, 'word/_rels/document.xml.rels')
    rid2file = dict(re.findall(r'Id="([^"]+)"[^>]*Target="media/([^"]+)"', rels))

    body = re.search(r'<w:body>([\s\S]*)</w:body>', xml).group(1)
    blocks = re.findall(r'<w:p\b[\s\S]*?</w:p>', body)

    sets, cur, started = [], None, False
    for b in blocks:
        t = text_of(b)
        imgs = [rid2file[i] for i in re.findall(r'r:embed="([^"]+)"', b) if i in rid2file]
        if re.match(r'^SPEAKING PART 2', t, re.I):
            started = True
            continue
        if not started:
            continue
        head = re.match(r'^(\d+)\.\s*Describe the picture(?:\s*\((\d+)\))?', t, re.I)
        if head:
            if cur:
                sets.append(cur)
            cur = {'id': 'p2-%02d' % int(head.group(1)), 'no': int(head.group(1)),
                   'bank': head.group(2) or '', 'img': '', 'tasks': []}
            cur['tasks'].append({'k': 'describe', 'q': 'Describe the picture.'})
            continue
        if cur is None:
            continue
        if imgs and not cur['img']:
            cur['img'] = imgs[0]
        if t and not re.match(r'^\d+\.\s*Describe', t, re.I):
            for line in t.split('\n'):
                line = line.strip()
                if line and len(cur['tasks']) < 3:
                    cur['tasks'].append({'k': 'q%d' % len(cur['tasks']), 'q': line})
    if cur:
        sets.append(cur)
    return sets


def shrink_images(sets):
    os.makedirs(MEDIA, exist_ok=True)
    with zipfile.ZipFile(P2_DOC) as z:
        for s in sets:
            if not s['img']:
                continue
            raw = z.read('word/media/' + s['img'])
            im = Image.open(io.BytesIO(raw)).convert('RGB')
            im.thumbnail((1100, 1100), Image.LANCZOS)
            name = '%02d.jpg' % s['no']
            im.save(os.path.join(MEDIA, name), 'JPEG', quality=72, optimize=True, progressive=True)
            s['img'] = 'media/part2/' + name


def write_js(path, varname, data, note):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('/* %s — sinh tự động bởi import-speaking.py, đừng sửa tay */\n' % note)
        f.write('window.%s = %s;\n' % (varname, json.dumps(data, ensure_ascii=False, indent=1)))


# Trong file gốc, bản trả lời thứ hai của hai câu này bị đặt nhầm ô:
# ô câu 15 chứa bản dành cho câu 14, ô câu 21 chứa bản dành cho câu 20.
ALT_MOVE = {'p1-15': 'p1-14', 'p1-21': 'p1-20'}


def fix_alt(p1):
    by = {x['id']: x for x in p1}
    for src, dst in ALT_MOVE.items():
        if src in by and dst in by and by[src].get('alt'):
            by[dst]['alt'] = by[src]['alt']
            by[src]['alt'] = ''
            print('  chuyen ban thu hai: %s -> %s' % (src, dst))
    return p1


if __name__ == '__main__':
    p1 = fix_alt(parse_part1())
    write_js(os.path.join(DATA, 'part1.js'), 'APTIS_PART1', p1, 'Aptis Speaking Part 1')
    print('Part 1: %d câu, %d mục từ vựng'
          % (len(p1), sum(len(x['vocab']) for x in p1)))
    for x in p1[:2]:
        print('  -', x['id'], '|', x['group'][:28], '|', x['q'][:46], '| %d từ' % len(x['answer'].split()))

    p2 = parse_part2()
    shrink_images(p2)
    write_js(os.path.join(DATA, 'part2.js'), 'APTIS_PART2', p2, 'Aptis Speaking Part 2')
    total = sum(os.path.getsize(os.path.join(MEDIA, f)) for f in os.listdir(MEDIA)) / 1048576
    print('Part 2: %d bộ, ảnh nén còn %.1f MB' % (len(p2), total))
    for x in p2[:3]:
        print('  -', x['id'], '|', x['img'], '|', ' // '.join(t['q'][:40] for t in x['tasks']))
