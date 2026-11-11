# 見本ページ（drafts/redesign.html）の文言を、上から順に一覧にして
# Googleスプレッドシート用の表（drafts/hitoiro-copy.xlsx）に書き出す
# 実行：python3 drafts/export_copy.py
import os, re
from bs4 import BeautifulSoup, NavigableString, Tag
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, 'drafts/redesign.html'), encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')

SECTIONS = ['ファーストビュー', '02 お悩み', '03 思い', '04 できること', '05 ステップ',
            '06 プラン', '07 名前', '08 プロフィール', '09 相談']
INLINE = {'em', 'br', 'b', 'strong'}

def is_inline(t):
    if isinstance(t, NavigableString):
        return True
    if t.name in INLINE:
        return all(is_inline(c) for c in t.children)
    if t.name == 'span' and set(t.get('class') or []) & {'wb', 'mk'} and not (set(t.get('class') or []) - {'wb', 'mk'}):
        return all(is_inline(c) for c in t.children)
    return False

def text_of(nodes):
    out = ''
    for n in nodes:
        if isinstance(n, NavigableString):
            out += str(n)
        elif n.name == 'br':
            out += '\n'
        else:
            out += text_of(n.children)
    return re.sub(r'[ \t\r\f\v]*\n[ \t\r\f\v]*', '\n', re.sub(r'[ \t]+', ' ', out)).strip()

def emphasis(nodes):
    words = []
    for n in nodes:
        if isinstance(n, Tag):
            if n.name == 'em':
                words.append(text_of(n.children))
            else:
                words += emphasis(n.children)
    return words

KIND = {'h1': 'キャッチ', 'h2': '見出し', 'h3': '小見出し', 'summary': '開閉ボタン', 'dt': '項目名',
        'dd': '説明', 'li': '項目', 'a': 'ボタン', 'small': '補足', 'b': '項目名', 'span': '説明', 'p': '文'}

def kind_of(el):
    cls = set(el.get('class') or [])
    if 'btn' in cls: return 'ボタン'
    if cls & {'r-label', 'role', 'service-label'}: return 'ラベル'
    if cls & {'role-title', 'own-title', 'r-lead', 'ask', 'first'}: return '小見出し'
    if 'nm-word' in cls or 'nm-yomi' in cls: return '名前'
    return KIND.get(el.name, '文')

rows = []
def walk(el, sec):
    if isinstance(el, NavigableString) or el.name in ('script', 'style', 'svg', 'img'):
        return
    cls = set(el.get('class') or [])
    if cls & {'num', 'hero-visual', 'crow', 'strip'} or el.get('aria-hidden') == 'true':
        return
    # まとめて1行にするもの
    if el.name == 'i' and el.parent.name == 'h3':
        return
    if el.name == 'li' and el.find_parent(class_='spot'):
        sp = el.find('span'); bb = el.find('b')
        rows.append([sec, '料金', text_of(sp.children) + '：' + text_of(bb.children).replace('\n', '／'), '「項目：金額」の形で'])
        return
    if el.name == 'li' and el.find_parent(class_='steps'):
        bb = el.find('b'); sp = el.find('span')
        rows.append([sec, '項目名', text_of(bb.children), '']); rows.append([sec, '説明', text_of(sp.children), ''])
        return
    if 'price' in cls:
        rows.append([sec, '料金', text_of(el.children), '数字は大きく表示']); return
    if el.name == 'div' and el.parent.name == 'dl' and el.find_parent(class_='tools'):
        rows.append([sec, '利用ツール', text_of(el.find('dt').children) + '：' + '、'.join(text_of(t.children) for t in el.find_all(class_='tool')), '「種類：ツール名、ツール名」の形で'])
        return
    if el.name == 'summary' and not text_of(el.children):
        return
    if el.name == 'summary' and el.find('small'):
        rows.append([sec, '開閉ボタン', text_of(el.find('span').children), '']); rows.append([sec, '補足', text_of(el.find('small').children), '']); return
    kids = list(el.children)
    own = [c for c in kids if is_inline(c)]
    rest = [c for c in kids if not is_inline(c)]
    txt = text_of(own)
    if txt and not (el.name == 'summary' and not txt):
        emp = emphasis(own)
        rows.append([sec, kind_of(el), txt, '大きく見せる言葉：' + '／'.join(emp) if emp else ''])
    for c in rest:
        walk(c, sec)

for i, sec in enumerate(soup.select('.page > section')):
    walk(sec, SECTIONS[i])

wb = Workbook(); ws = wb.active; ws.title = '文言'
ws.append(['HITO IRO トップページの文言一覧（見本 drafts/redesign.html より）'])
ws.append(['使い方：直したいところだけ、黄色の「新しい文言」の列に書いてください。空欄のところは今のまま。改行したい位置は、そのまま改行して大丈夫です。書き終わったら、Claude に「文言を反映して」と送ってください。'])
ws.append([])
ws.append(['番号', 'セクション', '種類', '今の文言', '新しい文言', 'メモ'])
for n, r in enumerate(rows, 1):
    sec_no = r[0][:2] if r[0][:2].isdigit() else '01'
    ws.append([f'{n:03d}', r[0], r[1], r[2], None, r[3]])

thin = Side(style='thin', color='DDDDDD')
ws['A1'].font = Font(bold=True, size=14, color='7B4FA0')
ws['A2'].alignment = Alignment(wrap_text=True, vertical='top')
ws.merge_cells('A2:F2'); ws.row_dimensions[2].height = 48
for c in ws[4]:
    c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='7B4FA0')
    c.alignment = Alignment(vertical='center')
yellow = PatternFill('solid', fgColor='FFF7CC')
for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical='top')
        c.border = Border(top=thin, bottom=thin)
    row[4].fill = yellow
for col, w in zip('ABCDEF', [6, 16, 10, 48, 48, 24]):
    ws.column_dimensions[col].width = w
ws.freeze_panes = 'A5'
out = os.path.join(ROOT, 'drafts/hitoiro-copy.xlsx')
wb.save(out)
print(len(rows), '件', out, os.path.getsize(out), 'bytes')
for r in rows: print(' | '.join(x.replace('\n', '⏎') for x in r))
