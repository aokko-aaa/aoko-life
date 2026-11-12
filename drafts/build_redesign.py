# 見本ページ（drafts/redesign.html）を、今の public/index.html から作る
# 色・フォント・ロゴ・カラス・似顔絵は今のヒトイロのまま。構成と見せ方だけ変えた見本。
# 実行：python3 drafts/build_redesign.py（見本）／ python3 drafts/build_redesign.py --publish（公開用の public/index.html）
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'drafts/base-index.html'), encoding='utf-8').read()  # 作り直す前のページ（画像やロゴの動きをここから取り出す）

def W(*xs):
    return ''.join(f'<span class="wb">{x}</span>' for x in xs)

def block(start_tag_pos, tag='div'):
    """start_tag_pos から始まる要素の終わりまでを返す"""
    depth = 0
    for m in re.finditer(rf'<(/?){tag}\b[^>]*>', src[start_tag_pos:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return src[start_tag_pos:start_tag_pos + m.end()]

head = src[:src.index('</style>')]
hero_visual = block(src.index('<div class="hero-visual">'))
portrait = re.search(r'<img class="portrait"[^>]*>', src).group(0)
footer = src[src.index('  <footer>'):src.index('</footer>') + len('</footer>')]
_s = src.rindex('<script>'); script = src[_s:src.index('</script>', _s) + len('</script>')]
career = block(src.index('<div class="career">'))
# 最後の相談セクションに添える花（最初の画面のカラスの頭の花と同じ絵）
_stem = re.search(r'<img class="crow-stem" src="([^"]+)"', src).group(1)
_head = re.search(r'<img class="crow-head" src="([^"]+)"', src).group(1)
FLOWER = f'<div class="cflower" aria-hidden="true"><img class="cf-stem" src="{_stem}" alt=""><img class="cf-head" src="{_head}" alt=""></div>'
career = career.replace('<dd><span class="tool">Microsoft Excel</span></dd>', '<dd><span class="tool">Google系ツール各種</span><span class="tool">Microsoft Excel</span></dd>')
more_body = block(src.index('<div class="more-body">'))

FORM = 'https://forms.gle/UdpYn5shPJjUKRza7'

CSS = r'''
  /* ===== 見本：参考LPの構成 × ヒトイロの色 ===== */
  :root{--soft-purple:#f3edf8;--pale-purple:#e4d7ef;--shadow:0 2px 10px rgba(123,79,160,.08);--shadow-float:0 2px 6px rgba(123,79,160,.06),0 16px 40px rgba(123,79,160,.14);}
  body{background:#ececee;}
  .page{background:transparent;border-top:0;padding:8px 8px 0;}
  .page > section{background:var(--paper);border-radius:20px;border-bottom:0;margin-bottom:8px;padding:56px 20px;}
  .page > section.gray{background:#f6f6f7;}
  .page > section.purple{background:linear-gradient(160deg,#9064b5 0%,#7b4fa0 55%,#6a4290 100%);color:var(--paper);}
  .num{color:var(--brand);}
  .purple .num{color:rgba(255,255,255,.75);}

  /* 見出し：キーワードだけ大きく紫、つなぎは小さく */
  .r-h{font-size:19px;font-weight:700;line-height:1.4;margin-bottom:28px;letter-spacing:.02em;}
  .r-h em{font-style:normal;font-size:28px;color:var(--brand);}
  .purple .r-h em{color:var(--paper);}
  .r-lead{font-weight:700;line-height:1.6;margin:-12px 0 24px;}

  /* ボタン：ピル型＋右に丸い矢印 */
  .btn{position:relative;padding-right:56px;padding-left:56px;box-shadow:var(--shadow-float);}
  .btn::after{content:"";position:absolute;right:8px;top:50%;width:36px;height:36px;margin-top:-18px;border-radius:50%;
    background:var(--paper) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 6l6 6-6 6' fill='none' stroke='%237b4fa0' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/18px no-repeat;}
  .btn-white{background:var(--paper);color:var(--brand);}
  .btn-white::after{background-color:var(--brand);background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 6l6 6-6 6' fill='none' stroke='%23fff' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");}

  /* ファーストビュー */
  #hero .catch{font-size:22px;}
  #hero .catch em{font-style:normal;font-size:32px;color:var(--brand);}
  .badges{display:grid;grid-template-columns:repeat(3,1fr);margin-top:28px;border-top:1px solid var(--line);padding-top:20px;}
  .badges > div{text-align:center;line-height:1.4;}
  .badges > div+div{border-left:1px solid var(--line);}
  .badges small{display:block;font-size:11px;color:var(--muted);font-weight:700;}
  .badges b{font-size:26px;color:var(--brand);letter-spacing:-.02em;}
  .badges span{font-size:12px;font-weight:700;}

  /* お悩み：吹き出し */
  .bubbles{display:grid;gap:12px;}
  .bubbles li{position:relative;background:var(--paper);border-radius:20px 20px 20px 4px;padding:14px 18px;font-weight:700;line-height:1.6;box-shadow:var(--shadow);width:fit-content;max-width:88%;}
  .bubbles li:nth-child(even){justify-self:end;border-radius:20px 20px 4px 20px;}
  .answer{margin-top:28px;display:flex;align-items:center;gap:12px;}
  .answer p{background:var(--brand);color:var(--paper);font-weight:700;line-height:1.6;border-radius:20px;padding:14px 20px;}

  /* 思い */
  .r-label{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.16em;color:var(--brand);background:var(--paper);border-radius:999px;padding:0 12px;line-height:1.8;margin-bottom:16px;}
  .ask{font-size:17px;font-weight:700;line-height:1.6;margin-bottom:28px;}
  .ask small{display:block;font-size:14px;font-weight:400;line-height:1.8;margin-top:8px;opacity:.9;}
  .split{display:grid;gap:10px;}
  .split > div{border-radius:24px;padding:24px 20px 20px;}
  .split .you{border:2px solid rgba(255,255,255,.55);}
  .split .us{background:var(--paper);color:var(--ink);box-shadow:var(--shadow-float);}
  .split .role{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.1em;line-height:1.8;border-radius:999px;padding:0 12px;background:rgba(255,255,255,.18);}
  .split .us .role{background:var(--soft-purple);color:var(--brand);}
  .split .role-title{font-size:22px;font-weight:700;line-height:1.4;margin:10px 0 14px;}
  .split .us .role-title{color:var(--brand);}
  .split li{position:relative;padding:12px 0 12px 22px;border-top:1px solid rgba(255,255,255,.25);}
  .split .us li{border-top-color:var(--line);}
  .split li::before{content:"";position:absolute;left:2px;top:19px;width:10px;height:10px;border-radius:50%;border:2px solid currentColor;opacity:.8;}
  .split .us li::before{border-color:var(--brand);}
  .split li b{display:block;font-size:15px;line-height:1.6;}
  .split li span{display:block;font-size:13px;line-height:1.6;opacity:.85;}
  .split .us li span{color:var(--muted);opacity:1;}
  .gains{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:28px;}
  .gains li{background:var(--paper);color:var(--ink);border-radius:16px;padding:16px 6px 14px;text-align:center;font-size:12px;font-weight:700;line-height:1.6;}
  .gains svg{width:36px;height:36px;color:var(--brand);display:block;margin:0 auto 6px;}
  .chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:20px;}
  .chips li{font-size:13px;font-weight:700;border:1px solid rgba(255,255,255,.6);border-radius:999px;padding:4px 12px;line-height:1.6;}
  .chips-p{margin-top:24px;font-weight:700;line-height:1.6;}
  .private{margin-top:12px;font-size:13px;line-height:1.8;opacity:.9;}

  /* できること */
  .motto-r{display:inline-block;font-weight:700;line-height:1.6;background:var(--soft-purple);color:var(--brand);border-radius:999px;padding:6px 16px;margin:-8px 0 24px;}
  .svc{display:grid;gap:12px;}
  .svc-card{background:#f9f8fa;border-radius:24px;padding:24px 20px;box-shadow:var(--shadow);}
  .svc-card h3{display:flex;align-items:center;gap:12px;color:var(--brand);font-size:17px;margin-bottom:14px;}
  .svc-card h3 i{flex:none;font-style:normal;width:40px;height:40px;border-radius:50%;background:var(--pale-purple);color:var(--brand);display:grid;place-items:center;font-size:18px;}
  .tags{display:flex;flex-wrap:wrap;gap:6px;}
  .tags li{font-size:13px;font-weight:700;line-height:1.6;background:var(--paper);border:1px solid var(--pale-purple);border-radius:999px;padding:4px 12px;}
  .ways-r{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:16px;}
  .ways-r li{display:grid;place-items:center;text-align:center;font-size:13px;font-weight:700;line-height:1.6;border:2px solid var(--brand);color:var(--brand);border-radius:16px;padding:10px 6px;}
  .before{margin-top:16px;font-size:13px;}
  .before summary{cursor:pointer;color:var(--muted);font-weight:700;min-height:44px;display:flex;align-items:center;gap:8px;list-style:none;}
  .before summary::-webkit-details-marker{display:none;}
  .before summary::after{content:"";width:7px;height:7px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg) translateY(-2px);}
  .before[open] summary::after{transform:rotate(-135deg);}
  .page > section.has-before{padding-bottom:40px;}
  .before p{color:var(--muted);line-height:1.8;}

  /* ステップ */
  .steps{counter-reset:s;display:grid;gap:10px;}
  .steps li{counter-increment:s;display:grid;grid-template-columns:44px 1fr;gap:14px;align-items:center;background:var(--paper);border-radius:16px;padding:14px 16px;box-shadow:var(--shadow);}
  .steps li{position:relative;}
  /* 線は丸の中心から次の丸の中心まで引き、丸の後ろに回す（丸と丸のあいだだけ見える） */
  .steps li:not(:last-child)::after{content:"";position:absolute;z-index:1;left:35px;top:50%;height:calc(100% + 10px);width:2px;background:var(--accent);transform-origin:top;}
  .js .steps li.reveal:not(:last-child)::after{transform:scaleY(0);transition:transform .9s ease .45s;}
  .js .steps li.reveal.is-in:not(:last-child)::after{transform:scaleY(1);}
  @media (prefers-reduced-motion: reduce){.js .steps li.reveal:not(:last-child)::after{transform:none;transition:none;}}
  .steps li::before{content:counter(s);box-sizing:border-box;position:relative;z-index:2;background:var(--paper);width:40px;height:40px;border-radius:50%;border:2px solid var(--brand);color:var(--brand);font-weight:700;display:grid;place-items:center;}
  .steps b{display:block;color:var(--brand);line-height:1.6;}
  .steps span{font-size:13px;color:var(--muted);line-height:1.6;}

  /* プラン */
  .plan-note{font-size:12px;line-height:1.8;opacity:.9;margin:-12px 0 20px;}
  .plans-r{display:grid;gap:10px;}
  .plan{background:var(--paper);color:var(--ink);border-radius:24px;padding:22px 20px;}
  .plan p:first-child{font-weight:700;color:var(--brand);}
  .price{font-weight:700;line-height:1.4;margin:4px 0 6px;}
  .price b{font-size:56px;color:var(--brand);letter-spacing:-.03em;}
  .price span{font-size:15px;}
  .plan small{font-size:13px;line-height:1.6;color:var(--muted);display:block;}
  .trial-r{margin-top:12px;border:2px solid rgba(255,255,255,.7);color:var(--paper);border-radius:999px;text-align:center;font-weight:700;line-height:1.6;padding:10px 12px;font-size:14px;}
  .spot{background:var(--paper);color:var(--ink);border-radius:24px;padding:20px;margin-top:10px;}
  .spot > p{font-weight:700;color:var(--brand);margin-bottom:6px;}
  .spot li{display:flex;justify-content:space-between;gap:12px;align-items:baseline;padding:10px 0;border-bottom:1px dashed var(--line);font-size:14px;line-height:1.6;}
  .spot li:last-child{border-bottom:0;}
  .spot li b{color:var(--brand);white-space:nowrap;text-align:right;}
  .first{margin:0 0 20px;font-weight:700;line-height:1.6;}
  .fold{margin-top:10px;}
  .fold summary{list-style:none;cursor:pointer;display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;min-height:60px;background:var(--paper);color:var(--brand);border-radius:20px;padding:14px 56px 14px 20px;position:relative;box-shadow:var(--shadow-float);}
  .fold summary::-webkit-details-marker{display:none;}
  .fold summary span{font-weight:700;font-size:16px;line-height:1.6;}
  .fold summary small{display:block;width:100%;font-size:12px;color:var(--muted);line-height:1.6;}
  .fold summary::after{content:"";position:absolute;right:16px;top:50%;width:28px;height:28px;margin-top:-14px;border-radius:50%;background:var(--brand) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 9l6 6 6-6' fill='none' stroke='%23fff' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/16px no-repeat;transition:transform .3s;}
  .fold[open] summary::after{transform:rotate(180deg);}
  .fold-body{padding-top:10px;}
  .fold .spot{margin-top:0;}
  @media (prefers-reduced-motion: reduce){.fold summary::after{transition:none;}}
  .first b{font-size:30px;}
  .purple .first{text-align:left;}

  /* 名前 */
  .names{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
  .names li{background:var(--soft-purple);border-radius:20px;padding:18px 14px;}
  .names b{display:block;color:var(--brand);font-size:16px;line-height:1.4;margin-bottom:6px;}
  .names span{font-size:12px;line-height:1.6;display:block;}
  .names-close{margin-top:20px;font-weight:700;line-height:1.6;text-align:center;}

  /* プロフィール */
  .prof-top{display:grid;grid-template-columns:96px 1fr;gap:16px;align-items:center;margin-bottom:20px;}
  .prof-top .portrait{width:96px;height:96px;border-radius:50%;margin:0;}
  .prof-top b{display:block;color:var(--brand);line-height:1.6;}
  .prof-top span{font-size:13px;line-height:1.6;}
  .prof-msg{background:var(--paper);border-radius:24px 24px 24px 4px;padding:18px 20px;line-height:1.8;box-shadow:var(--shadow);}
  #profile-r .more summary{margin-top:8px;}
  #profile-r .career{margin-top:16px;}

  /* 相談 */
  #contact-r{text-align:center;}
  #contact-r .r-h{margin-bottom:12px;}
  #contact-r .btn{margin-top:28px;}

  @media (min-width: 900px){
    .page{padding:10px 10px 0;}
    .page > section{border-radius:24px;padding:110px max(64px, calc((100% - 1040px) / 2));}
    .r-h{font-size:32px;margin-bottom:44px;}
    .r-h em{font-size:46px;}
    #hero .catch{font-size:30px;white-space:nowrap;}
    #hero .catch em{font-size:44px;}
    #hero .hero-visual{grid-row:1 / span 5;}
    .badges{max-width:460px;}
    .badges b{font-size:32px;}
    .bubbles{grid-template-columns:repeat(3,1fr);gap:16px;}
    .bubbles li,.bubbles li:nth-child(even){justify-self:stretch;max-width:none;width:auto;border-radius:24px 24px 24px 4px;}
    .answer{justify-content:center;}
    .ask{font-size:22px;}
    .split{grid-template-columns:1fr 1fr;gap:16px;text-align:left;}
    .split > div{padding:32px 32px 24px;}
    .split .role-title{font-size:28px;}
    .gains{gap:16px;}
    .gains li{font-size:15px;padding:28px 12px;}
    .gains svg{width:64px;height:64px;}
    .svc{grid-template-columns:repeat(3,1fr);gap:16px;}
    .ways-r{max-width:640px;}
    .steps{grid-template-columns:repeat(5,1fr);}
    .steps li{grid-template-columns:1fr;justify-items:center;text-align:center;padding:24px 12px;}
    .steps li:not(:last-child)::after{left:50%;top:43px;height:2px;width:calc(100% + 16px);transform-origin:left;}
    .js .steps li.reveal:not(:last-child)::after{transform:scaleX(0);}
    .js .steps li.reveal.is-in:not(:last-child)::after{transform:scaleX(1);}
    /* 1→5へ順番に：1本ずつ、左から右へつながって走る */
    .js .steps li.reveal:not(:last-child)::after{transition:transform .45s linear .5s;}
    .js .steps li.reveal:nth-child(2):not(:last-child)::after{transition-delay:.95s;}
    .js .steps li.reveal:nth-child(3):not(:last-child)::after{transition-delay:1.4s;}
    .js .steps li.reveal:nth-child(4):not(:last-child)::after{transition-delay:1.85s;}
    @media (prefers-reduced-motion: reduce){.js .steps li.reveal:not(:last-child)::after{transform:none;transition:none;}}
    .steps{gap:16px;}
    .plans-r{grid-template-columns:1fr 1fr;gap:16px;}
    .fold{max-width:760px;margin-left:auto;margin-right:auto;}
    .purple .first{text-align:center;}
    .price b{font-size:72px;}
    .spot ul{columns:2;column-gap:40px;}
    .spot li{break-inside:avoid;}
    .names{grid-template-columns:repeat(4,1fr);gap:16px;}
    #profile-r .prof-wrap{max-width:640px;margin:0 auto;}
    .page > section.purple:not(#contact-r) > p, .page > section .r-label{display:block;text-align:center;}
    .page > section .r-label{width:fit-content;margin-left:auto;margin-right:auto;}
    .chips{justify-content:center;}
    .motto-r{display:block;width:fit-content;margin-left:auto;margin-right:auto;}
    .ways-r{margin-left:auto;margin-right:auto;}
    .before{text-align:center;}
    .before summary{justify-content:center;}
    #contact-r .btn{width:360px;margin:32px auto 0;}
  }

  /* ===== 角丸・札・影を減らして、落ち着いた見た目に ===== */
  .page > section{border-radius:6px;}
  .btn{box-shadow:none;}
  .btn::after{background:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 6l6 6-6 6' fill='none' stroke='%23fff' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:center;background-size:18px;}
  .btn-white::after{background-color:transparent;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 6l6 6-6 6' fill='none' stroke='%237b4fa0' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");}
  /* お悩み：吹き出し → 黄緑の線つきの一行 */
  .bubbles{gap:0;}
  .bubbles li, .bubbles li:nth-child(even){justify-self:stretch;width:auto;max-width:none;background:none;box-shadow:none;border-radius:0;padding:14px 0 14px 16px;border-left:3px solid var(--accent);border-bottom:1px solid var(--line);}
  .answer p{background:none;color:var(--brand);padding:0;border-radius:0;font-size:17px;}
  /* ラベル・札 → ふつうの文字 */
  .r-label, .split .role, .split .us .role{background:none;border-radius:0;padding:0;color:inherit;opacity:.85;}
  .split .us .role{color:var(--brand);}
  .chips{gap:0;}
  .chips li{border:0;border-radius:0;padding:0;}
  .chips li+li::before{content:"／";margin:0 8px;opacity:.6;}
  .motto-r{background:none;border-radius:0;padding:0 0 0 12px;border-left:3px solid var(--accent);}
  .tags{display:grid;grid-template-columns:1fr 1fr;gap:0 16px;}
  .tags li{background:none;border:0;border-top:1px solid var(--line);border-radius:0;padding:8px 0;font-weight:500;}
  .svc-card h3 i{background:none;width:auto;height:auto;font-size:26px;border-radius:0;}
  .ways-r li{border:0;border-top:2px solid var(--brand);border-radius:0;padding:10px 0 0;}
  /* 箱：角丸を小さく、影なし */
  .split > div, .gains li, .svc-card, .steps li, .plan, .spot, .names li, .prof-msg{border-radius:6px;box-shadow:none;}
  .split .us{box-shadow:none;}
  .trial-r{border:0;border-top:1px solid rgba(255,255,255,.5);border-bottom:1px solid rgba(255,255,255,.5);border-radius:0;}
  .fold summary{border-radius:6px;box-shadow:none;}
  .fold summary::after{background-color:transparent;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 9l6 6 6-6' fill='none' stroke='%237b4fa0' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");}
  /* 「続きを読む」など → 下線つきの文字 */
  #profile-r .more summary{border:0;border-radius:0;padding:0;margin:0;justify-content:flex-start;min-height:44px;text-decoration:underline;text-underline-offset:6px;}
  .tool{border-radius:4px !important;}
  @media (min-width: 900px){
    .page > section{border-radius:8px;}
    .bubbles{grid-template-columns:repeat(3,1fr);gap:0 24px;}
    .bubbles li, .bubbles li:nth-child(even){border-radius:0;}
    .tags{grid-template-columns:1fr;}
  }

  /* 開閉の目印は、下向きの三角だけ */
  .more summary::after, .before summary::after{width:0;height:0;border:0;border-left:6px solid transparent;border-right:6px solid transparent;border-top:8px solid currentColor;transform:none;transition:transform .25s ease;}
  .more[open] summary::after, .before[open] summary::after{transform:rotate(180deg);}
  #profile-r .more summary{text-decoration:none;color:var(--brand);gap:10px;}
  #profile-r .more summary.tri-only{justify-content:center;width:100%;}
  .fold summary::after{width:0;height:0;margin-top:-4px;right:22px;background:none;border-left:7px solid transparent;border-right:7px solid transparent;border-top:9px solid var(--brand);border-radius:0;}
  @media (prefers-reduced-motion: reduce){.more summary::after,.before summary::after{transition:none;}}

  /* 02 の答えの補足 */
  .answer small{display:block;font-size:14px;font-weight:400;color:var(--ink);line-height:1.8;margin-top:6px;}
  /* ヒトイロの仕事：番号つきの流れ */
  .route{counter-reset:r;}
  .split .route li{counter-increment:r;padding-left:34px;}
  .split .route li::before{content:counter(r);border:0;opacity:1;width:24px;height:24px;top:13px;left:0;border-radius:50%;background:var(--brand);color:var(--paper);font-size:12px;font-weight:700;display:grid;place-items:center;}
  /* 事業者らしさ */
  .own{margin-top:32px;padding:24px 0 0;border-top:1px solid rgba(255,255,255,.4);}
  .own-title{font-size:20px;font-weight:700;line-height:1.4;margin-bottom:8px;}
  .own p+p{line-height:1.8;}
  @media (min-width: 900px){
    .own{max-width:760px;margin-left:auto;margin-right:auto;text-align:center;}
    .own-title{font-size:26px;}
    .answer{flex-direction:column;}
    .answer p{text-align:center;}
  }

  /* 07 名前：HITO × IRO */
  .nm{display:grid;gap:8px;}
  .nm-word{font-size:56px;font-weight:700;line-height:1;letter-spacing:.06em;color:var(--ink);}
  .nm-iro .nm-word{color:var(--brand);}
  .nm-yomi{font-size:12px;font-weight:700;color:var(--muted);letter-spacing:.4em;margin:8px 0 14px;}
  .nm dl div{display:grid;grid-template-columns:5em 1fr;gap:12px;align-items:baseline;padding:12px 0;border-top:1px solid var(--line);}
  .nm dl div:last-child{border-bottom:1px solid var(--line);}
  .nm dt{font-weight:700;font-size:17px;line-height:1.4;}
  .nm-iro dt{color:var(--brand);}
  .nm dd{font-size:14px;line-height:1.6;}
  .nm-x{font-size:32px;color:var(--gray);line-height:1;text-align:center;margin:12px 0;}
  .strip{display:flex;height:16px;margin:44px 0 18px;}
  .strip i{flex:1;background:#dcdcdf;}
  .strip i:nth-child(2){background:#c9c9cd;}
  .strip i:nth-child(3){background:#b8b8bd;}
  .strip i:nth-child(4){background:#a6a6ac;}
  .strip i:nth-child(5){background:#949494;}
  .strip .add{flex:1.2;background:var(--brand);transform-origin:left;}
  .js .strip.reveal{opacity:1;transform:none;}
  .js .strip.reveal .add{transform:scaleX(0);transition:transform 1s cubic-bezier(.4,0,.2,1) .6s;}
  .js .strip.reveal.is-in .add{transform:scaleX(1);}
  @media (prefers-reduced-motion: reduce){.js .strip.reveal .add{transform:none;transition:none;}}
  .names-close{font-size:17px;}
  @media (min-width: 900px){
    .nm{grid-template-columns:1fr auto 1fr;gap:48px;align-items:start;}
    .nm-word{font-size:80px;}
    .nm-x{margin:22px 0 0;font-size:40px;}
    .strip{max-width:760px;margin:64px auto 20px;height:20px;}
    .names-close{font-size:22px;}
  }

  /* 03 思い：薄いラベンダー → 紫へ、ふわっと色が変わる */
  #omoi.purple{background:#eeeaf3;color:var(--ink);position:relative;isolation:isolate;transition:color 2.4s ease .5s;}
  #omoi::before{content:"";position:absolute;inset:0;z-index:-1;border-radius:inherit;background:linear-gradient(160deg,#9064b5 0%,#7b4fa0 55%,#6a4290 100%);opacity:0;transition:opacity 3.6s ease;}
  #omoi .r-h em, #omoi .split .you, #omoi .split .you li, #omoi .own, #omoi .r-label{transition:color 2.4s ease .5s, border-color 2.4s ease .5s;}
  #omoi .r-h em{color:var(--brand);}
  #omoi .r-label{color:var(--brand);}
  #omoi .split .you{border-color:rgba(123,79,160,.35);}
  #omoi .split .you li{border-top-color:rgba(123,79,160,.18);}
  #omoi .own{border-top-color:rgba(123,79,160,.25);}
  #omoi.lit::before, html:not(.js) #omoi::before{opacity:1;}
  #omoi.lit, html:not(.js) #omoi.purple{color:var(--paper);}
  #omoi.lit .r-h em, #omoi.lit .r-label{color:var(--paper);}
  #omoi.lit .split .you{border-color:rgba(255,255,255,.55);}
  #omoi.lit .split .you li{border-top-color:rgba(255,255,255,.25);}
  #omoi.lit .own{border-top-color:rgba(255,255,255,.4);}
  @media (prefers-reduced-motion: reduce){
    #omoi.purple, #omoi::before, #omoi .r-h em, #omoi .split .you, #omoi .split .you li, #omoi .own, #omoi .r-label{transition:none;}
  }

  /* ボタンの中の小さな添え書き（匿名OK） */
  .btn-sub{font-size:12px;font-weight:700;letter-spacing:.04em;margin-left:10px;opacity:.85;}

  /* ===== つなぎ目のない1枚のページに ===== */
  .page{padding:0;}
  .page > section, .page > section.gray, .page > section.purple{border-radius:0;margin-bottom:0;}
  /* 最初の画面：カラスとロゴはいちばん下。絵の下の端は、ぼかして次のセクションに溶けこませる */
  #hero{padding-bottom:0;}
  #hero .btn{margin-top:28px;}
  #hero .hero-visual{margin:12px 0 0;}
  #hero .crow{
    -webkit-mask-image:linear-gradient(to right, transparent 0, #000 14%), linear-gradient(to bottom, #000 72%, transparent 100%);
    -webkit-mask-composite:source-in;
            mask-image:linear-gradient(to right, transparent 0, #000 14%), linear-gradient(to bottom, #000 72%, transparent 100%);
            mask-composite:intersect;
  }
  @media (min-width: 900px){
    #hero{display:block;position:relative;min-height:min(760px, calc(100vh - 0px));padding:140px 64px 140px max(64px, calc((100% - 1152px) / 2));}
    #hero > *{max-width:520px;position:relative;z-index:2;}
    #hero .hero-visual{position:absolute;right:0;bottom:0;width:min(60%, 820px);max-width:none;margin:0;z-index:1;}
    #hero .crow{width:56%;margin-right:0;}
    /* ロゴはカラスに重ねすぎない：少し小さくして左へ（カラスとは端が少し重なるくらい） */
    #hero .logo-write{left:-14%;width:72%;top:40%;}
    #hero .btn{margin-top:44px;}
  }

  /* 大きく見せる言葉の中の、補助のひらがなは小さく（まわりの文字と同じくらい） */
  em .s{font-size:.68em;}

  /* グレーのセクションは、上の端を白からなめらかにグレーへ（前の白いセクションとの境目をなくす） */
  .page > section.gray{background:linear-gradient(var(--paper) 0, #f6f6f7 140px);}

  /* 09 相談：花を添える（動かさない。スマホは右上、パソコンは文字とボタンの右側） */
  #contact-r{position:relative;}
  .cflower{position:absolute;right:12px;top:20px;width:92px;aspect-ratio:260/232;margin:0;overflow:hidden;}
  .cflower img{position:absolute;left:-113.85%;top:-3.45%;width:230.77%;height:auto;max-width:none;}
  .cflower{-webkit-mask-image:linear-gradient(to bottom,#000 80%,transparent 100%);mask-image:linear-gradient(to bottom,#000 80%,transparent 100%);}
  @media (min-width: 900px){.cflower{left:calc(50% + 230px);right:auto;top:auto;bottom:90px;width:170px;}}
  .js .cflower .cf-stem{clip-path:inset(40% 0 0 0);transform:scale(.25);transform-origin:66% 38%;}
  .js .cflower .cf-head{transform:scale(0) rotate(-40deg);opacity:0;transform-origin:69% 21%;}
  .js .cflower.grow .cf-stem{animation:sprout 1.8s cubic-bezier(.3,.6,.3,1) .2s forwards;}
  .js .cflower.grow .cf-head{animation:bloom 1.1s cubic-bezier(.3,1.4,.5,1) 1.8s forwards;}
  @media (prefers-reduced-motion: reduce){.js .cflower .cf-stem,.js .cflower .cf-head{clip-path:none;transform:none;opacity:1;animation:none;}}

  /* ===== 09 相談：縦幅をせまく／花が咲いたら、白い液体がはじけて色が反転する ===== */
  .page > section#contact-r{padding-top:44px;padding-bottom:44px;overflow:hidden;isolation:isolate;}
  #contact-r > *:not(.splash){position:relative;z-index:2;}
  #contact-r .cflower{position:absolute;z-index:3;}
  /* スマホ：文字は中央揃え、花は見出しの右の空き */
  #contact-r{text-align:center;}
  .cflower{left:auto;right:6px;top:26px;width:76px;}
  #contact-r .btn{margin-top:20px;}
  /* はじける白い液体 */
  .splash{position:absolute;inset:0;z-index:1;pointer-events:none;}
  .splash .blob{position:absolute;left:var(--fx,80%);top:var(--fy,30%);width:var(--sz,300vmax);height:var(--sz,300vmax);margin:calc(var(--sz,300vmax) / -2) 0 0 calc(var(--sz,300vmax) / -2);
    background:var(--paper);border-radius:43% 57% 54% 46% / 47% 41% 59% 53%;transform:scale(0);}
  .splash .drop{position:absolute;left:var(--fx,80%);top:var(--fy,30%);width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:var(--paper);opacity:0;}
  .splash .drop:nth-child(odd){width:9px;height:9px;margin:-4.5px 0 0 -4.5px;}
  #contact-r.pop .blob{animation:splash-blob 1.9s cubic-bezier(.55,.05,.3,1) forwards;}
  #contact-r.pop .drop{animation:splash-drop 1.1s cubic-bezier(.2,.8,.3,1) .15s forwards;}
  @keyframes splash-blob{
    0%{transform:scale(0) rotate(0deg);}
    35%{border-radius:62% 38% 46% 54% / 38% 60% 40% 62%;}
    70%{border-radius:48% 52% 60% 40% / 56% 44% 56% 44%;}
    100%{transform:scale(1) rotate(35deg);border-radius:50%;}
  }
  @keyframes splash-drop{
    0%{opacity:1;transform:rotate(var(--a)) translateX(0) scale(1);}
    100%{opacity:0;transform:rotate(var(--a)) translateX(150px) scale(.3);}
  }
  /* 色の反転（背景が白になるのに合わせて） */
  #contact-r .r-h, #contact-r .r-h em, #contact-r > p{transition:color .7s ease .5s;}
  #contact-r .btn{transition:background-color .7s ease .5s, color .7s ease .5s;}
  #contact-r.pop .r-h{color:var(--ink);}
  #contact-r.pop .r-h em{color:var(--brand);}
  #contact-r.pop > p{color:var(--ink);}
  #contact-r.pop .btn{background-color:var(--brand);color:var(--paper);}
  #contact-r.pop .btn::after{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 6l6 6-6 6' fill='none' stroke='%23fff' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");}
  @media (min-width: 900px){
    .page > section#contact-r{padding-top:72px;padding-bottom:72px;}
    .cflower{left:calc(50% + 230px);right:auto;top:auto;bottom:56px;width:170px;}
    #contact-r .btn{margin-top:28px;}
  }

  /* ===== キャッチを大きく／最初の画面の相談ボタンを少し小さく ===== */
  #hero .catch{font-size:min(24px, 6.4vw);}
  #hero .catch em{font-size:min(36px, 9.6vw);}
  #hero .btn{width:100%;max-width:300px;min-height:50px;font-size:15px;}
  @media (min-width: 900px){
    #hero > *{max-width:580px;}
    #hero .catch{font-size:38px;}
    #hero .catch em{font-size:60px;}
    #hero .btn{width:300px;min-height:54px;font-size:16px;}
  }

  /* 03 思いのアイコン：カードが表示されたら、時間差で動き、約4秒ごとにくり返す（左から順に） */
  .gains li:nth-child(1){--o:.2s;} .gains li:nth-child(2){--o:.6s;} .gains li:nth-child(3){--o:1s;}
  .gains svg{width:48px;height:48px;}
  @media (min-width: 900px){.gains svg{width:64px;height:64px;}}
  .js .gains li.reveal .ia{transform-box:fill-box;}
  .js .gains li.reveal .b1{transform-origin:20% 100%;transform:scale(0);}
  .js .gains li.reveal .b2{transform-origin:80% 100%;transform:scale(0);}
  .js .gains li.reveal .dot{transform-origin:50% 50%;transform:scale(0);}
  .js .gains li.reveal .head{transform-origin:100% 0;transform:scale(0);}
  .js .gains li.reveal .ray, .js .gains li.reveal .line{stroke-dasharray:1;stroke-dashoffset:1;}
  .js .gains li.reveal.is-in .b1{animation:ico-pop-loop 4s ease var(--o) infinite both;}
  .js .gains li.reveal.is-in .b2{animation:ico-pop-loop2 4s ease var(--o) infinite both;}
  .js .gains li.reveal.is-in .dot{animation:ico-pop-loop 4s ease var(--o) infinite both;}
  .js .gains li.reveal.is-in .ray{animation:ico-draw-loop2 4s ease-out var(--o) infinite both;}
  .js .gains li.reveal.is-in .line{animation:ico-draw-loop 4s ease-in-out var(--o) infinite both;}
  .js .gains li.reveal.is-in .head{animation:ico-pop-loop3 4s ease var(--o) infinite both;}
  /* 出る → 止まる → すっと消える をくり返す */
  @keyframes ico-pop-loop{0%{transform:scale(0);}10%{transform:scale(1.18);}15%{transform:scale(1);}82%{transform:scale(1);}92%,100%{transform:scale(0);}}
  @keyframes ico-pop-loop2{0%,9%{transform:scale(0);}19%{transform:scale(1.18);}24%{transform:scale(1);}82%{transform:scale(1);}92%,100%{transform:scale(0);}}
  @keyframes ico-pop-loop3{0%,19%{transform:scale(0);}27%{transform:scale(1.2);}32%{transform:scale(1);}82%{transform:scale(1);}92%,100%{transform:scale(0);}}
  @keyframes ico-draw-loop{0%{stroke-dashoffset:1;}20%{stroke-dashoffset:0;}82%{stroke-dashoffset:0;}92%,100%{stroke-dashoffset:1;}}
  @keyframes ico-draw-loop2{0%,9%{stroke-dashoffset:1;}20%{stroke-dashoffset:0;}82%{stroke-dashoffset:0;}92%,100%{stroke-dashoffset:1;}}
  @media (prefers-reduced-motion: reduce){
    .js .gains li.reveal .ia{transform:none;stroke-dashoffset:0;animation:none !important;}
  }

  /* 03 思い：人を雇う場合との比較（軽く） */
  .vs{margin-top:32px;}
  .vs-title{font-size:15px;font-weight:700;line-height:1.6;margin-bottom:12px;}
  .vs-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
  .vs-grid > div{border-radius:6px;padding:14px 12px;}
  .vs-hire{border:1px solid rgba(123,79,160,.3);transition:border-color 2.4s ease .5s;}
  #omoi.lit .vs-hire{border-color:rgba(255,255,255,.45);}
  .vs-us{background:var(--paper);color:var(--ink);}
  .vs-grid p{font-size:13px;font-weight:700;line-height:1.6;margin-bottom:6px;}
  .vs-us p{color:var(--brand);}
  .vs-grid li{font-size:12px;line-height:1.6;padding:6px 0;border-top:1px solid rgba(127,127,127,.25);}
  .vs-hire li{opacity:.9;}
  @media (min-width: 900px){
    .vs{max-width:760px;margin:44px auto 0;}
    .vs-title{text-align:center;font-size:17px;margin-bottom:16px;}
    .vs-grid{gap:16px;text-align:left;}
    .vs-grid > div{padding:20px 24px;}
    .vs-grid p{font-size:15px;}
    .vs-grid li{font-size:14px;}
  }
'''

ICON = lambda d: ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" '
                  'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>')
talk = ICON('<path class="ia b1" d="M8 12h22v14H18l-6 5v-5H8z"/><path class="ia b2" d="M30 18h10v13h-3v5l-6-5h-9" stroke="#b4ff3f"/>')
spark = ICON('<path class="ia ray" pathLength="1" d="M24 14V6"/><path class="ia ray" pathLength="1" d="M24 34v8"/><path class="ia ray" pathLength="1" d="M14 24H6"/><path class="ia ray" pathLength="1" d="M34 24h8"/><circle class="ia dot" cx="24" cy="24" r="6" stroke="#b4ff3f"/>')
arrow = ICON('<path class="ia line" pathLength="1" d="M8 38l12-12 7 7 13-15"/><path class="ia head" d="M32 18h8v8" stroke="#b4ff3f"/>')

BODY = f'''
<div class="page">

  <!-- 01 ファーストビュー -->
  <section id="hero">
    <p class="service-label">あれこれサポート<span>HITO IRO（ヒトイロ）</span></p>
    <h1 class="catch"><em>あとひとり</em>、<br>一緒に<em>動<span class="s">ける</span>人</em>が<span class="wb">いたら。</span></h1>
    <p class="sub">事業のとなりに、もうひといろ。</p>
    <a class="btn" href="{FORM}" target="_blank" rel="noopener">まずは話してみる</a>
    {hero_visual}
  </section>

  <!-- 02 お悩み -->
  <section class="gray">
    <span class="num">02</span>
    <h2 class="r-h"><span class="mk">その<em>「あれこれ」</em>、<br>ひとりで<em>抱<span class="s">えて</span></em><span class="wb">いませんか？</span></span></h2>
    <ul class="bubbles">
      <li>{W("何から始めよう…")}</li>
      <li>{W("考えが、","形にならない")}</li>
      <li>{W("雑用で、","本業が後回しに")}</li>
      <li>{W("人を増やすのは、","ためらう")}</li>
      <li>{W("ちょっと","相談したい")}</li>
      <li>{W("AIを使いたいけど…")}</li>
    </ul>
    <div class="answer"><p>{W("ひとりで抱えなくて、","大丈夫です！")}<small>{W("お話をしながら、","一緒にボトルネックを","探っていきましょう。")}</small></p></div>
  </section>

  <!-- 03 思い（スクロールすると、薄いラベンダーから紫へふわっと変わる） -->
  <section class="purple" id="omoi">
    <span class="r-label">HITO IROの思い</span>
    <h2 class="r-h"><em>あなた<span class="s">にしか</span></em><br><span class="wb">できない仕事に、</span><br><em>あなた<span class="s">の</span>時間</em>を。</h2>
    <p class="ask">{W("お客さまが待っているのは、","あなたです。")}<small>{W("だからヒトイロは、","作業を代わるだけでなく、")}{W("事業の全体を一緒に見て、","あなたの時間を奪っている","ボトルネックを見つけ、","ほどいていきます。")}</small></p>
    <div class="split">
      <div class="you">
        <p class="role">あなたの仕事</p>
        <p class="role-title">{W("前に立って、","決める。")}</p>
        <ul>
          <li><b>お客さまとの対話</b><span>接客・提案・信頼づくり</span></li>
          <li><b>商品・サービスを磨く</b><span>よりよくする・新しく生み出す</span></li>
          <li><b>次の一手を決める</b><span>事業の方向・優先順位の判断</span></li>
        </ul>
      </div>
      <div class="us">
        <p class="role">ヒトイロの仕事</p>
        <p class="role-title">{W("全体を見て、","流れを整える。")}</p>
        <ol class="route">
          <li><b>全体を見わたす</b><span>{W("業務の棚卸し、","時間の使い方の見える化")}</span></li>
          <li><b>ボトルネックを見つける</b><span>{W("止まっているところ、","詰まっているところを","一緒に探す")}</span></li>
          <li><b>ほどいて、整える</b><span>{W("手順や仕組み、","ツールの見直し")}</span></li>
          <li><b>実務まで動く</b><span>{W("事務・資料・発信など、","手を動かす部分も")}</span></li>
        </ol>
      </div>
    </div>
    <ul class="gains">
      <li>{talk}{W("信頼が","深まる")}</li>
      <li>{spark}{W("新しい企画が","動く")}</li>
      <li>{arrow}{W("事業が","前へ進む")}</li>
    </ul>
    <div class="own">
      <p class="own-title">{W("あなたの事業らしさは、","そのままに。")}</p>
      <p>{W("決まったやり方を押しつけず、","今ある色を活かしながら、","もうひといろを添えます。")}</p>
    </div>
    <div class="vs">
      <p class="vs-title">{W("人を雇うのと、","くらべると")}</p>
      <div class="vs-grid">
        <div class="vs-hire"><p>人を増やすと</p><ul>
          <li>{W("求人・面接・教育に、","時間と手間がかかる")}</li>
          <li>{W("仕事が少ない月も、","人件費は毎月かかる")}</li>
          <li>{W("一度雇うと、","気軽には減らせない")}</li>
        </ul></div>
        <div class="vs-us"><p>ヒトイロなら</p><ul>
          <li>{W("採用の手間をかけずに、","相談できる")}</li>
          <li>{W("必要な仕事から、","小さく頼める")}</li>
          <li>{W("手が空いた分、","本来の仕事に","集中できる")}</li>
        </ul></div>
      </div>
    </div>
    <p class="private">{W("本来の業務に集中して、","事業の成長に","力を注ぐことができるように。")}</p>
  </section>

  <!-- 04 できること -->
  <section class="has-before">
    <span class="num">04</span>
    <h2 class="r-h"><span class="mk"><em>できること</em>は、<br>大きく<em>3<span class="s">つ</span></em>。</span></h2>
    <p class="motto-r">効率はAIで。彩りは人で。</p>
    <div class="svc">
      <div class="svc-card"><h3><i>A</i>頭の中の「あれこれ」</h3>
        <ul class="tags"><li>業務の棚卸し</li><li>ボトルネック探し</li><li>壁打ち・相談</li><li>アイデアの言語化</li><li>優先順位の整理</li><li>やることリスト化</li></ul></div>
      <div class="svc-card"><h3><i>B</i>日々の仕事の「あれこれ」</h3>
        <ul class="tags"><li>事務サポート</li><li>リサーチ・比較資料</li><li>SNS運用</li><li>デザイン・文章</li><li>イラスト</li><li>進捗管理</li><li>マニュアル整備</li></ul></div>
      <div class="svc-card"><h3><i>C</i>AIで効率化</h3>
        <ul class="tags"><li>下調べ・資料づくり</li><li>定型業務の見直し</li><li>ツール導入の一歩目</li></ul></div>
    </div>
    <ul class="ways-r"><li>{W("まるっと","お任せ")}</li><li>{W("自分たちで","回せるように")}</li></ul>
    <details class="before"><summary>ご依頼の前に</summary>
      <p>{W("本格的なホームページ制作や","システム構築は、","専門の方に委託して","進めることもあります。")}{W("日常的な現場のお手伝いは、","たまになら喜んで。")}</p></details>
  </section>

  <!-- 05 ステップ -->
  <section class="gray">
    <span class="num">05</span>
    <h2 class="r-h"><span class="mk"><em>5<span class="s">つ</span></em>のステップで、<br><span class="wb">一緒に進めます。</span></span></h2>
    <ol class="steps">
      <li><div><b>話す</b><span>頭の中を、そのまま話す</span></div></li>
      <li><div><b>整理する</b><span>進む方向を見つける</span></div></li>
      <li><div><b>段取りを組む</b><span>具体的な行動に変える</span></div></li>
      <li><div><b>実行する</b><span>実務まで引き受ける</span></div></li>
      <li><div><b>振り返る</b><span>次の一歩を決める</span></div></li>
    </ol>
  </section>

  <!-- 06 プラン -->
  <section class="purple">
    <span class="num">06</span>
    <h2 class="r-h"><em>プラン</em></h2>
    <p class="plan-note">{W("税込・目安です。","内容や量に応じて、","ご相談のうえ決定します。")}</p>
    <p class="first">相談は <b>無料</b></p>
    <details class="fold">
      <summary><span>月額でお任せ</span><small>スタンダード・フルサポート</small></summary>
      <div class="fold-body">
    <div class="plans-r">
      <div class="plan"><p>スタンダード</p><p class="price"><b>6</b><span>万円/月</span></p><small>思考の整理から実務まで、まるごと</small></div>
      <div class="plan"><p>フルサポート</p><p class="price"><b>9</b><span>万円/月</span></p><small>{W("現場でのお手伝いも。","（西三河/名古屋方面のみ）")}</small></div>
    </div>
    <p class="trial-r">{W("はじめての方は、","1ヶ月だけ3.5万円で","お試しOK（1回限り）")}</p>
      </div>
    </details>
    <details class="fold">
      <summary><span>スポット</span><small>これだけ頼みたいとき</small></summary>
      <div class="fold-body">
    <div class="spot">
      <ul>
        <li><span>リサーチ・比較資料</span><b>1万5,000円〜</b></li>
        <li><span>販促物の作成（印刷費別）</span><b>1万円〜</b></li>
        <li><span>イラスト制作</span><b>5,000円〜</b></li>
        <li><span>SNS運用サポート</span><b>3万5,000円〜</b></li>
        <li><span>AI使い方相談（1対1）</span><b>1時間5,000円〜<br>3時間まで10,000円</b></li>
      </ul>
    </div>
      </div>
    </details>
  </section>

  <!-- 07 名前 -->
  <section>
    <span class="num">07</span>
    <h2 class="r-h"><span class="mk"><em>HITO IRO</em>という名前</span></h2>
    <div class="nm">
      <div class="nm-col nm-hito">
        <p class="nm-word">HITO</p><p class="nm-yomi">ヒト</p>
        <dl>
          <div><dt>人</dt><dd>{W("人それぞれ、","会社それぞれの","個性を大切に")}</dd></div>
          <div><dt>ひとり</dt><dd>{W("もうひとり加わることで、","新しい視点を")}</dd></div>
          <div><dt>人の温度</dt><dd>{W("AIを使っても、","温かさは失わない")}</dd></div>
        </dl>
      </div>
      <p class="nm-x" aria-hidden="true">×</p>
      <div class="nm-col nm-iro">
        <p class="nm-word">IRO</p><p class="nm-yomi">イロ</p>
        <dl>
          <div><dt>色</dt><dd>{W("その事業だけが持つ、","今ある色")}</dd></div>
          <div><dt>ひといろ</dt><dd>{W("そこに加わる、","新しい彩り")}</dd></div>
          <div><dt>彩る</dt><dd>{W("塗り替えずに、","一色を添える")}</dd></div>
        </dl>
      </div>
    </div>
    <div class="strip" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i class="add"></i></div>
    <p class="names-close">{W("事業の色を塗り替えない。","もうひといろを添える。")}</p>
  </section>

  <!-- 08 プロフィール -->
  <section class="gray" id="profile-r">
    <span class="num">08</span>
    <h2 class="r-h"><span class="mk"><em>プロフィール</em></span></h2>
    <div class="prof-wrap">
      <div>
        <div class="prof-top">{portrait}<div><b>クリエイティブサポーター</b></div></div>
        <p class="prof-msg">{W("「やりたい」が","いつも頭の中で大渋滞。")}{W("わたし自身がそんなタイプだから、","アイデアを抱える方の気持ちが","よくわかります。")}</p>
        <details class="more"><summary class="tri-only" aria-label="続きを読む"></summary>{more_body}</details>
      </div>
      <details class="more more-career"><summary>経歴・利用ツール</summary>{career}</details>
    </div>
  </section>

  <!-- 09 相談 -->
  <section class="purple" id="contact-r">
    <div class="splash" aria-hidden="true"><i class="blob"></i><i class="drop" style="--a:-20deg"></i><i class="drop" style="--a:35deg"></i><i class="drop" style="--a:95deg"></i><i class="drop" style="--a:150deg"></i><i class="drop" style="--a:200deg"></i><i class="drop" style="--a:255deg"></i><i class="drop" style="--a:310deg"></i></div>
    {FLOWER}
    <h2 class="r-h">その<em>「あれこれ」</em>、<br><span class="wb">聞かせてください。</span></h2>
    <p>まとまっていなくても大丈夫です。</p>
    <a class="btn btn-white" href="{FORM}" target="_blank" rel="noopener">相談フォームへ<small class="btn-sub">仮名OK</small></a>
  </section>

{footer}
</div>
'''

js = script.replace(
    script[script.index("document.querySelectorAll(\n"):script.index(");", script.index("document.querySelectorAll(\n")) + 2],
    "document.querySelectorAll('#hero > *, .page > section > .r-h, .own, .vs, .nm-col, .strip, .bubbles li, .answer, .split > div, .gains li, .svc-card, .steps li, .plan, .spot, .names li, .prof-msg, #contact-r > p, #contact-r .btn');")

import sys
PUBLISH = '--publish' in sys.argv  # 付けると public/index.html（公開用）に書き出す。付けないと見本（drafts/redesign.html）
if not PUBLISH:
    head = re.sub(r'<title>(.*?)</title>', r'<title>【見本】\1</title>', head, count=1)
    head = head.replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1)
OMOI_JS = r'''
<script>
  // 09 相談の花：画面に少しでも入ったら、絵の読み込みを待ってから、芽が伸びて花が咲く（いちど咲いたらそのまま）
  (function(){
    var f = document.querySelector('.cflower');
    if (!f) return;
    var started = false;
    var start = function(){
      if (started) return; started = true;
      var imgs = Array.prototype.slice.call(f.querySelectorAll('img'));
      Promise.all(imgs.map(function(img){
        return img.decode ? img.decode().catch(function(){}) : Promise.resolve();
      })).then(function(){ requestAnimationFrame(function(){
        f.classList.add('grow');
        var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (still) return;
        setTimeout(function(){
          var sec = document.getElementById('contact-r');
          var r = f.getBoundingClientRect(), b = sec.getBoundingClientRect();
          // 花の中心（花びらのあたり）から、はじける
          sec.style.setProperty('--fx', (r.left - b.left + r.width * 0.3) + 'px');
          sec.style.setProperty('--fy', (r.top - b.top + r.height * 0.3) + 'px');
          // セクション全体をちょうど覆えるくらいの大きさ（大きすぎると一瞬で白くなるため）
          sec.style.setProperty('--sz', (Math.hypot(b.width, b.height) * 2.3) + 'px');
          sec.classList.add('pop');
        }, 2700);
      }); });
    };
    if (!('IntersectionObserver' in window)) { start(); return; }
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting) { start(); io.disconnect(); } });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0 });
    io.observe(f);
  })();
</script>

<script>
  // 03 思い：セクションの上の端が画面の中ほどまで来たら紫に。上に戻ると薄い色に戻る
  (function(){
    var sec = document.getElementById('omoi');
    if (!sec) return;
    if (!('IntersectionObserver' in window)) { sec.classList.add('lit'); return; }
    new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting) sec.classList.add('lit');
        else if (e.boundingClientRect.top > 0) sec.classList.remove('lit');
      });
    }, { rootMargin: '0px 0px -55% 0px', threshold: 0 }).observe(sec);
  })();
</script>'''
out = head + CSS + '</style>\n</head>\n<body>' + BODY + js + OMOI_JS + '\n</body>\n</html>\n'
dest = 'public/index.html' if PUBLISH else 'drafts/redesign.html'
open(os.path.join(ROOT, dest), 'w', encoding='utf-8').write(out)
print('書き出しました：' + dest, len(out))
