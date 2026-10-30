"""my pouch のページを書き出す。

pouch/tools.json（道具のデータ）を読んで、
  public/pouch/index.html            … 一覧ページ
  public/pouch/<slug>/index.html     … 道具ごとのページ
を作り直す。道具を足したり直したりしたら、リポジトリの一番上で
  python3 pouch/build.py
を実行する。手で public/pouch/ の html を直さないこと（次に書き出したとき消える）。
"""

import json
import re
import shutil
import zipfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "pouch" / "tools.json"
OUT = ROOT / "public" / "pouch"
SITE = "https://life.aokoworks.workers.dev"

REQUIRED = ["name", "slug", "tsumari", "description", "date", "published"]

try:
    # 日本語を文節（意味のまとまり）で区切る道具。なくても動くが、改行が少し雑になる
    #   入れ方： pip install budoux
    import budoux
    _parser = budoux.load_default_japanese_parser()
except ImportError:
    _parser = None


def wb(text):
    """言葉の途中で改行されないようにする（index.html と同じ <span class="wb"> の方法）。
    まず読点・句点で区切り、それでも1行に収まらないときは文節の切れ目で折り返す。
    データの文に「|」を入れると、そこでも区切る（折り返してほしい場所の目印。ページには出ない）。"""
    clauses = [c for seg in text.split("|")
               for c in re.findall(r"[^、。！？]*[、。！？]+[」』）]*|[^、。！？]+$", seg)]
    out = []
    for c in clauses:
        if not c:
            continue
        phrases = _parser.parse(c) if _parser else [c]
        inner = "".join(f'<span class="wb">{escape(p)}</span>' for p in phrases) if len(phrases) > 1 else escape(c)
        out.append(f'<span class="wb">{inner}</span>')
    return "".join(out)


SKILLS = ROOT / "pouch" / "skills"

DEFAULT_STEPS = [
    "zipをダウンロードして、解凍します。",
    "Claude CodeやCodexに、そのフォルダを読ませます。",
    "「このスキルで自分用のアプリを作って」と頼みます。",
]


def make_skill_zip(slug):
    """pouch/skills/<slug>/ があれば、中身を public/pouch/files/<slug>-skills.zip にまとめる。
    zip の中の日付は固定にして、中身が同じなら毎回同じファイルになるようにする。"""
    src = SKILLS / slug
    if not src.is_dir():
        return ""
    rel = f"pouch/files/{slug}-skills.zip"
    dest = ROOT / "public" / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src.rglob("*")):
            if f.is_file() and not f.name.startswith("."):
                info = zipfile.ZipInfo(f"{slug}-skills/{f.relative_to(src).as_posix()}", (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                info.flag_bits |= 0x800  # 日本語のファイル名を文字化けさせない
                z.writestr(info, f.read_bytes())
    return rel


def file_exists(rel):
    """public/ からの相対パス（例 pouch/files/x.zip）のファイルが実際にあるか"""
    return bool(rel) and (ROOT / "public" / rel.lstrip("/")).is_file()


CSS = """
  :root{
    --ink:#333333;
    --paper:#fff;
    --line:#dcdcdc;
    --muted:#666;
    --soft:#f4f4f4;
    --brand:#7b4fa0;
    --accent:#b4ff3f;   /* 黄緑：文字には使わず、帯や線だけ */
    --lav:#957bb1;      /* my pouch のラベンダー */
    --deep:#4a4660;     /* my pouch のこい紫 */
    --lav-soft:#f3eff7;
    --max:440px;
    --gutter:20px;
  }
  *{box-sizing:border-box;margin:0;padding:0;}
  body{font-family:'Noto Sans JP',sans-serif;background:var(--soft);color:var(--ink);line-height:1.8;font-size:15px;-webkit-text-size-adjust:100%;}
  .page{max-width:var(--max);margin:0 auto;background:var(--paper);min-height:100vh;border-top:8px solid var(--accent);}
  .wb{display:inline-block;}
  a{color:var(--brand);}
  .topnav{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:6px var(--gutter);border-bottom:1px solid var(--line);}
  .topnav a{display:inline-flex;align-items:center;gap:8px;min-height:48px;text-decoration:none;}
  .topnav .home img{width:96px;height:auto;display:block;}
  .topnav .home span{font-size:11px;color:var(--muted);line-height:1.3;}
  .topnav .to-list{font-size:13px;font-weight:700;color:var(--deep);}
  .topnav .to-list img{width:22px;height:22px;}
  .hitoiro-banner{margin:48px var(--gutter) 0;padding:24px 20px;border:2px solid var(--brand);border-radius:6px;text-align:center;}
  .hitoiro-banner .by{font-size:12px;color:var(--muted);}
  .hitoiro-banner img{width:150px;height:auto;display:block;margin:6px auto 4px;}
  .hitoiro-banner .svc{font-size:13px;font-weight:700;color:var(--brand);letter-spacing:.08em;}
  .hitoiro-banner .catch{font-weight:700;font-size:16px;line-height:1.6;margin:10px 0 16px;}
  main{padding:32px var(--gutter) 48px;}
  .pouch-head{display:flex;align-items:center;gap:14px;margin-bottom:20px;}
  .pouch-head{margin-top:20px;}
  .pouch-icon{position:relative;width:72px;height:72px;flex:none;}
  .pouch-icon img{width:72px;height:72px;display:block;position:relative;z-index:1;}
  /* あめちゃん：ポーチの口から飛び出して、まわりに落ち着く */
  .candy{position:absolute;left:24px;top:6px;width:24px;height:12px;z-index:2;
    transform:translate(var(--x),var(--y)) rotate(var(--r));}
  .candy svg{display:block;width:100%;height:100%;}
  .c1{--x:-22px;--y:-14px;--r:-28deg;}
  .c2{--x:6px;--y:-26px;--r:12deg;}
  .c3{--x:36px;--y:-10px;--r:34deg;}
  @media (prefers-reduced-motion: no-preference){
    .candy{animation:pop 1.1s cubic-bezier(.25,.9,.35,1.15) both;}
    .c1{animation-delay:.5s;}
    .c2{animation-delay:.75s;}
    .c3{animation-delay:1s;}
    .pouch-icon img{animation:wiggle .9s ease .35s both;}
  }
  @keyframes pop{
    0%{transform:translate(0,12px) rotate(0) scale(.2);opacity:0;}
    25%{opacity:1;}
    55%{transform:translate(calc(var(--x) * .7),calc(var(--y) - 14px)) rotate(calc(var(--r) * 2)) scale(1);}
    100%{transform:translate(var(--x),var(--y)) rotate(var(--r)) scale(1);opacity:1;}
  }
  @keyframes wiggle{0%,100%{transform:rotate(0);}25%{transform:rotate(-6deg);}50%{transform:rotate(5deg);}75%{transform:rotate(-2deg);}}
  h1{font-size:26px;font-weight:700;line-height:1.35;color:var(--deep);}
  .pouch-head h1{font-size:30px;letter-spacing:.02em;}
  .lead{margin-bottom:28px;}
  .lead p+p{margin-top:8px;}
  .cards{list-style:none;display:grid;gap:14px;}
  .card{display:block;border:2px solid var(--lav);border-radius:6px;overflow:hidden;text-decoration:none;color:var(--ink);background:var(--paper);}
  .card img{display:block;width:100%;height:auto;border-bottom:1px solid var(--line);}
  .card-name{font-size:20px;font-weight:700;line-height:1.4;color:var(--paper);background:var(--brand);padding:12px 18px;}
  .card-body{padding:14px 18px 16px;}
  .card-tsumari{font-size:14px;line-height:1.7;}
  .card-more{display:block;margin-top:10px;font-size:13px;font-weight:700;color:var(--brand);}
  .empty{color:var(--muted);}
  .hero-img{display:block;width:100%;height:auto;border-radius:6px;margin-bottom:20px;}
  .tool-label{display:inline-block;font-size:12px;font-weight:700;color:var(--paper);background:var(--lav);padding:0 10px;border-radius:999px;margin-bottom:8px;}
  section{margin-top:32px;}
  h2{font-size:18px;font-weight:700;line-height:1.5;margin-bottom:12px;padding-left:12px;border-left:4px solid var(--accent);}
  .tsumari{background:var(--lav-soft);border-radius:6px;padding:16px 18px;font-weight:700;line-height:1.7;margin:16px 0;}
  .btn{display:flex;align-items:center;justify-content:center;min-height:52px;padding:12px 20px;background:var(--brand);color:var(--paper);font-weight:700;font-size:15px;letter-spacing:.06em;text-decoration:none;border-radius:999px;}
  .btn-sub{background:var(--paper);color:var(--brand);border:2px solid var(--brand);}
  .btn-off{background:var(--soft);color:var(--muted);border:2px dashed var(--line);cursor:default;}
  .note{font-size:13px;color:var(--muted);margin-top:8px;}
  .steps{list-style:none;counter-reset:step;margin:16px 0 12px;display:grid;gap:10px;}
  .steps li{counter-increment:step;display:grid;grid-template-columns:28px 1fr;gap:10px;align-items:start;font-size:14px;}
  .steps li::before{content:counter(step);width:28px;height:28px;border-radius:50%;background:var(--deep);color:var(--paper);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;margin-top:1px;}
  .tools{font-size:13px;color:var(--muted);margin-top:10px;}
  .enjoy{font-size:14px;}
  .skill-note{font-size:13px;background:var(--lav-soft);border-radius:6px;padding:12px 14px;margin-bottom:12px;}
  .notes{list-style:none;display:grid;gap:8px;}
  .notes a{display:flex;align-items:center;min-height:48px;padding:10px 14px;border:1px solid var(--line);border-radius:6px;text-decoration:none;color:var(--ink);font-size:14px;line-height:1.6;}
  .notes a::after{content:"";flex:none;margin-left:auto;padding-left:10px;width:8px;height:8px;border-right:2px solid var(--brand);border-top:2px solid var(--brand);transform:rotate(45deg);}
  .notes .src{display:block;font-size:11px;color:var(--muted);}
  .back{margin-top:40px;text-align:center;font-size:14px;}
  .back a{display:inline-flex;align-items:center;min-height:44px;}
  footer{padding:24px var(--gutter);text-align:center;font-size:12px;color:var(--muted);border-top:1px solid var(--line);}
  footer a{color:var(--muted);display:inline-flex;align-items:center;min-height:44px;}
  /* パソコン用（画面の幅が900px以上のときだけ）。スマホの見え方は変えない */
  @media (min-width: 900px){
    :root{--max:760px;--gutter:48px;}
    body{font-size:16px;}
    main{padding:48px var(--gutter) 64px;}
    .cards{grid-template-columns:1fr 1fr;}
    .hitoiro-banner{max-width:520px;margin:56px auto 0;}
    .btn{max-width:420px;margin-left:auto;margin-right:auto;}
  }
"""


def head(title, description, url, image):
    description = description.replace("|", "")
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="page">
"""


def candy(cls, body, stripe):
    """ラッピングされた、あめちゃんの絵"""
    return (f'        <span class="candy {cls}" aria-hidden="true"><svg viewBox="0 0 40 20">'
            f'<path d="M11 10 1 2.5 3.5 10 1 17.5Z" fill="#4a4660"/>'
            f'<path d="M29 10 39 2.5 36.5 10 39 17.5Z" fill="#4a4660"/>'
            f'<ellipse cx="20" cy="10" rx="10.5" ry="8" fill="{body}"/>'
            f'<path d="M14 4.5c3 3 3 8 0 11M20 2.2c3 3.5 3 12 0 15.6M26 4.5c3 3 3 8 0 11" stroke="{stripe}" stroke-width="1.6" fill="none"/>'
            f'</svg></span>')


CANDIES = "\n".join([
    candy("c1", "#aef63d", "#4a4660"),
    candy("c2", "#957bb1", "#ffffff"),
    candy("c3", "#f5a623", "#ffffff"),
])

TOPNAV_HOME = """  <nav class="topnav">
    <a class="home" href="/" aria-label="HITO IRO のトップへ"><img src="/pouch/hitoiro-logo.webp" alt="hitoiro" width="360" height="105"><span>あれこれサポート<br>トップへ</span></a>
"""

TOPNAV_LIST = """    <a class="to-list" href="/pouch/"><img src="/pouch/mypouch-icon-64.png" alt="" width="22" height="22">my pouch</a>
"""

BANNER = """  <aside class="hitoiro-banner">
    <p class="by">my pouch をつくっている</p>
    <img src="/pouch/hitoiro-logo.webp" alt="hitoiro" width="360" height="105" loading="lazy">
    <p class="svc">あれこれサポート</p>
    <p class="catch"><span class="wb">頭の中の「あれこれ」を、</span><span class="wb">一緒にカタチに。</span></p>
    <a class="btn btn-sub" href="/">HITO IRO を見る</a>
  </aside>
"""

FOOT = """  <footer>
    <p><a href="/">HITO IRO（あれこれサポート）</a></p>
    <p>© AOKOWORKS</p>
  </footer>
</div>
</body>
</html>
"""


def image_url(tool):
    return f"/{tool['image'].lstrip('/')}" if file_exists(tool.get("image")) else ""


def build_index(tools):
    title = "my pouch｜HITO IRO"
    desc = "暮らしのちょっとした不便を解決した、「あめちゃん」をおひとつどうぞ。"
    cards = []
    for t in tools:
        img = image_url(t)
        img_tag = f'<img src="{img}" alt="" loading="lazy">' if img else ""
        cards.append(f"""      <li>
        <a class="card" href="/pouch/{t['slug']}/">
          {img_tag}
          <p class="card-name">{escape(t['name'])}</p>
          <div class="card-body">
            <p class="card-tsumari">{wb(t.get('summary') or t['tsumari'])}</p>
            <span class="card-more">くわしく見る</span>
          </div>
        </a>
      </li>""")
    body = "\n".join(cards) if cards else '      <li class="empty">道具は準備中です。</li>'
    return head(title, desc, f"{SITE}/pouch/", f"{SITE}/pouch/og.png") + TOPNAV_HOME + "  </nav>\n" + f"""  <main>
    <div class="pouch-head">
      <div class="pouch-icon">
        <img src="/pouch/mypouch-icon.png" alt="" width="72" height="72">
{CANDIES}
      </div>
      <h1>my pouch</h1>
    </div>
    <div class="lead">
      <p>{wb('暮らしのちょっとした不便を解決した、')}<br>{wb('「あめちゃん」をおひとつどうぞ。')}</p>
      <p>{wb('気になるものがあれば、自由に使ってください。')}</p>
    </div>
    <ul class="cards">
{body}
    </ul>
  </main>
""" + BANNER + FOOT


def build_tool(t):
    title = f"{t['name']}｜my pouch"
    img = image_url(t)
    og = f"{SITE}{img}" if img else f"{SITE}/pouch/og.png"
    parts = []
    if img:
        parts.append(f'    <img class="hero-img" src="{img}" alt="">')
    parts.append(f"""    <span class="tool-label">my pouch</span>
    <h1>{escape(t['name'])}</h1>
    <p class="tsumari">{wb(t['tsumari'])}</p>
    <p>{wb(t['description'])}</p>""")

    if t.get("app_url"):
        parts.append(f"""    <section>
      <h2>すぐ使いたい方</h2>
      <a class="btn" href="{escape(t['app_url'])}" target="_blank" rel="noopener">アプリを開く</a>
      <p class="note">{wb('スマホやパソコンのブラウザで、そのまま使えます。')}</p>
    </section>""")

    steps = "\n".join(f"        <li><span>{wb(x)}</span></li>" for x in (t.get("skill_steps") or DEFAULT_STEPS))
    note = t.get("skill_note") or []
    if isinstance(note, str):
        note = [note]
    skill_note = f'      <p class="skill-note">{"<br>".join(wb(x) for x in note)}</p>' if note else ""
    zip_ok = file_exists(t.get("skill_zip"))
    if zip_ok:
        dl = f'<a class="btn btn-sub" href="/{t["skill_zip"].lstrip("/")}" download>スキルをダウンロード</a>'
    else:
        dl = '<span class="btn btn-off" aria-disabled="true">スキルは準備中です</span>'
    tools_line = ""
    if t.get("tools"):
        tools_line = f'<p class="tools">使えるツール：{escape("、".join(t["tools"]))}</p>'
    parts.append(f"""    <section>
      <h2>自分で作りたい方</h2>
      <p>{wb('スキルは、AIに作り方を教えるための説明書のようなファイルです。')}</p>
      <ol class="steps">
{steps}
      </ol>
{skill_note}
      <p class="enjoy">{wb('仕様を好みにカスタマイズしたり、デザインを変えたりして楽しんでください。')}</p>
      <div style="margin-top:16px">{dl}</div>
      {tools_line}
    </section>""")

    notes = [n for n in t.get("notes", []) if n.get("title") and n.get("url")]
    if notes:
        items = "\n".join(
            f'        <li><a href="{escape(n["url"])}" target="_blank" rel="noopener"><span>{escape(n["title"])}<span class="src">note</span></span></a></li>'
            for n in notes)
        parts.append(f"""    <section>
      <h2>くわしくはnoteで</h2>
      <ul class="notes">
{items}
      </ul>
    </section>""")

    parts.append("""    <p class="back"><a href="/pouch/">my pouch の一覧へ</a></p>""")
    return head(title, t["tsumari"], f"{SITE}/pouch/{t['slug']}/", og) + TOPNAV_HOME + TOPNAV_LIST + """  </nav>
  <main>
""" + "\n".join(parts) + """
  </main>
""" + BANNER + FOOT


def main():
    tools = json.loads(DATA.read_text(encoding="utf-8"))
    for t in tools:
        missing = [k for k in REQUIRED if t.get(k) in (None, "")]
        if missing:
            raise SystemExit(f"{t.get('name', '?')}: 必須の項目がありません → {', '.join(missing)}")
        if not re.fullmatch(r"[a-z0-9-]+", t["slug"]):
            raise SystemExit(f"{t['name']}: slug は英小文字・数字・ハイフンだけにしてください → {t['slug']}")
    for t in tools:
        z = make_skill_zip(t["slug"])
        if z and not t.get("skill_zip"):
            t["skill_zip"] = z
    shown = sorted((t for t in tools if t["published"] is True), key=lambda t: t["date"], reverse=True)

    # 公開しない・消した道具の古いページを残さないよう、道具ページのフォルダを作り直す
    keep = {"files", "images"}
    for d in OUT.iterdir():
        if d.is_dir() and d.name not in keep:
            shutil.rmtree(d)

    (OUT / "index.html").write_text(build_index(shown), encoding="utf-8")
    for t in shown:
        d = OUT / t["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(build_tool(t), encoding="utf-8")
    print(f"書き出しました：一覧と道具 {len(shown)} 件（非公開 {len(tools) - len(shown)} 件）")


if __name__ == "__main__":
    main()
