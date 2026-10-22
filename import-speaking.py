# -*- coding: utf-8 -*-
"""Trích dữ liệu Speaking Part 1 & 2 từ hai file .docx sang dữ liệu cho công cụ.

Chạy:  python import-speaking.py
Sinh ra:
  data/part1.js        21 câu hỏi Part 1 kèm chiến lược, mẫu trả lời, từ vựng
  data/part2.js        17 bộ Part 2 kèm 3 nhiệm vụ, phần trả lời để trống
  media/part2/NN.jpg   ảnh đã nén cho Part 2
"""
import datetime, io, json, os, re, zipfile
from PIL import Image

PIC_STAMP = datetime.datetime.now().strftime('%Y%m%d%H%M')

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'Input doc', 'Speaking')
P1_DOC = os.path.join(SRC, 'M- Aptis_Speaking_Part_1_Chuan_B2_Updated.docx')
P2_DOC = os.path.join(SRC, 'VMEC_Speaking Aptis - Part 1-2 (apdate 08.10).docx')
P3_DOC = os.path.join(SRC, 'VMEC_Speaking Aptis - Parrt 3 (updated 08.10).docx')
DATA = os.path.join(HERE, 'data')
MEDIA = os.path.join(HERE, 'media')

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


# ---------- Part 2 & 3: đề có tranh ----------
# Part 2 một tranh, Part 3 hai tranh để so sánh; cấu trúc còn lại giống nhau.
HEAD_P2 = re.compile(r'^(\d+)\.\s*Describe the picture(?:\s*\((\d+)\))?', re.I)
HEAD_P3 = re.compile(r'^(\d+)\.\s*(?:Describe (?:the )?(?:2|two) pictures?'
                     r'|Tell me what you see in the two pictures)(?:\s*\((\d+)\))?', re.I)


def parse_picture_part(doc, part, head_re, first_task):
    xml = xml_of(doc)
    rels = xml_of(doc, 'word/_rels/document.xml.rels')
    rid2file = dict(re.findall(r'Id="([^"]+)"[^>]*Target="media/([^"]+)"', rels))
    body = re.search(r'<w:body>([\s\S]*)</w:body>', xml).group(1)
    blocks = re.findall(r'<w:p\b[\s\S]*?</w:p>', body)

    sets, cur, started = [], None, False
    for b in blocks:
        t = text_of(b)
        imgs = []
        for d in re.findall(r'<w:drawing>.*?</w:drawing>', b, re.S):
            rid = re.search(r'r:embed="([^"]+)"', d)
            if not rid or rid.group(1) not in rid2file:
                continue
            # Word cắt ảnh bằng srcRect (đơn vị 1/1000 %) chứ không sửa file gốc
            m = re.search(r'<a:srcRect([^/>]*)/>', d)
            crop = {}
            if m:
                for k, v in re.findall(r'\b([ltrb])="(-?\d+)"', m.group(1)):
                    crop[k] = int(v) / 100000.0
            imgs.append({'src': rid2file[rid.group(1)], 'crop': crop})
        if re.match(r'^SPEAKING PART %d' % part, t, re.I):
            started = True
            continue
        if not started:
            continue
        head = head_re.match(t)
        if head:
            if cur:
                sets.append(cur)
            # đánh số lại theo thứ tự xuất hiện: file gốc có số trùng và nhảy cóc
            cur = {'no': len(sets) + 1, 'label': head.group(1),
                   'bank': head.group(2) or '', 'imgs': [], 'tasks': [{'k': 'describe', 'q': first_task}]}
            cur['id'] = 'p%d-%02d' % (part, cur['no'])
            continue
        if cur is None:
            continue
        cur['imgs'] += imgs
        if t and not head_re.match(t):
            for line in t.split('\n'):
                line = line.strip()
                if line and len(cur['tasks']) < 3:
                    cur['tasks'].append({'k': 'q%d' % len(cur['tasks']), 'q': line})
    if cur:
        sets.append(cur)
    return sets


def shrink_images(doc, sets, part):
    outdir = os.path.join(MEDIA, 'part%d' % part)
    os.makedirs(outdir, exist_ok=True)
    with zipfile.ZipFile(doc) as z:
        for s in sets:
            names = []
            for j, ref in enumerate(s['imgs']):
                raw = z.read('word/media/' + ref['src'])
                im = Image.open(io.BytesIO(raw)).convert('RGB')
                c = ref.get('crop') or {}
                if c:
                    w, h = im.size
                    box = (int(w * c.get('l', 0)), int(h * c.get('t', 0)),
                           int(w * (1 - c.get('r', 0))), int(h * (1 - c.get('b', 0))))
                    if box[2] - box[0] > 20 and box[3] - box[1] > 20:
                        im = im.crop(box)
                        print('  cat anh %s cho bo %d: %dx%d -> %dx%d'
                              % (ref['src'], s['no'], w, h, im.size[0], im.size[1]))
                im.thumbnail((1100, 1100), Image.LANCZOS)
                name = '%02d%s.jpg' % (s['no'], 'ab'[j] if len(s['imgs']) > 1 else '')
                im.save(os.path.join(outdir, name), 'JPEG', quality=72, optimize=True, progressive=True)
                names.append('media/part%d/%s' % (part, name))
            s['imgs'] = names


def write_js(path, varname, data, note, stamp=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('/* %s — sinh tự động bởi import-speaking.py, đừng sửa tay */\n' % note)
        f.write('window.%s = %s;\n' % (varname, json.dumps(data, ensure_ascii=False, indent=1)))
        if stamp:
            # mốc này gắn vào đường dẫn ảnh để trình duyệt không dùng bản cũ trong cache
            f.write("window.APTIS_PIC_VER = '%s';\n" % stamp)


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

    for part, doc, head, first in (
            (2, P2_DOC, HEAD_P2, 'Describe the picture.'),
            (3, P3_DOC, HEAD_P3, 'Tell me what you see in the two pictures.')):
        sets = parse_picture_part(doc, part, head, first)
        shrink_images(doc, sets, part)
        write_js(os.path.join(DATA, 'part%d.js' % part), 'APTIS_PART%d' % part, sets,
                 'Aptis Speaking Part %d' % part, stamp=PIC_STAMP)
        d = os.path.join(MEDIA, 'part%d' % part)
        mb = sum(os.path.getsize(os.path.join(d, f)) for f in os.listdir(d)) / 1048576
        nimg = sum(len(s['imgs']) for s in sets)
        print('Part %d: %d bộ, %d ảnh nén còn %.1f MB' % (part, len(sets), nimg, mb))
        bad = [s['id'] for s in sets if len(s['tasks']) != 3 or not s['imgs']]
        if bad:
            print('  CAN XEM LAI:', ', '.join(bad))
        for x in sets[:2]:
            print('  -', x['id'], '|', ','.join(x['imgs']), '|',
                  ' // '.join(t['q'][:38] for t in x['tasks']))
