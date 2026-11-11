# 見本ページ（drafts/redesign.html）を、今の public/index.html から作る
# 色・フォント・ロゴ・カラス・似顔絵は今のヒトイロのまま。構成と見せ方だけ変えた見本。
# 実行：python3 drafts/build_redesign.py
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'public/index.html'), encoding='utf-8').read()

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
  .steps li:not(:last-child)::after{content:"";position:absolute;z-index:1;left:35px;top:54px;height:calc(100% - 40px + 10px - 14px + 14px);width:2px;background:var(--accent);transform-origin:top;}
  .js .steps li.reveal:not(:last-child)::after{transform:scaleY(0);transition:transform .9s ease .45s;}
  .js .steps li.reveal.is-in:not(:last-child)::after{transform:scaleY(1);}
  @media (prefers-reduced-motion: reduce){.js .steps li.reveal:not(:last-child)::after{transform:none;transition:none;}}
  .steps li::before{content:counter(s);width:40px;height:40px;border-radius:50%;border:2px solid var(--brand);color:var(--brand);font-weight:700;display:grid;place-items:center;}
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
    .gains svg{width:48px;height:48px;}
    .svc{grid-template-columns:repeat(3,1fr);gap:16px;}
    .ways-r{max-width:640px;}
    .steps{grid-template-columns:repeat(5,1fr);}
    .steps li{grid-template-columns:1fr;justify-items:center;text-align:center;padding:24px 12px;}
    .steps li:not(:last-child)::after{left:calc(50% + 22px);top:44px;height:2px;width:calc(100% + 16px - 44px);transform-origin:left;}
    .js .steps li.reveal:not(:last-child)::after{transform:scaleX(0);}
    .js .steps li.reveal.is-in:not(:last-child)::after{transform:scaleX(1);}
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
'''

ICON = lambda d: ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.5" '
                  'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>')
talk = ICON('<path d="M8 12h22v14H18l-6 5v-5H8z"/><path d="M30 18h10v13h-3v5l-6-5h-9" stroke="#b4ff3f"/>')
spark = ICON('<path d="M24 6v8M24 34v8M6 24h8M34 24h8"/><circle cx="24" cy="24" r="6" stroke="#b4ff3f"/>')
arrow = ICON('<path d="M8 38l12-12 7 7 13-15"/><path d="M32 18h8v8" stroke="#b4ff3f"/>')

BODY = f'''
<div class="page">

  <!-- 01 ファーストビュー -->
  <section id="hero">
    <p class="service-label">あれこれサポート<span>HITO IRO（ヒトイロ）</span></p>
    <h1 class="catch"><em>あとひとり</em>、<br>一緒に<em>動ける人</em>が<span class="wb">いたら。</span></h1>
    <p class="sub">事業のとなりに、もうひといろ。</p>
    {hero_visual}
    <a class="btn" href="{FORM}" target="_blank" rel="noopener">まずは相談する</a>
  </section>

  <!-- 02 お悩み -->
  <section class="gray">
    <span class="num">02</span>
    <h2 class="r-h"><span class="mk">その<em>「あれこれ」</em>、<br>ひとりで<em>抱えて</em><span class="wb">いませんか？</span></span></h2>
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

  <!-- 03 思い -->
  <section class="purple">
    <span class="r-label">HITO IROの思い</span>
    <h2 class="r-h"><em>あなたにしか</em><br><span class="wb">できない仕事に、</span><br><em>あなたの時間</em>を。</h2>
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
    <p class="chips-p">{W("採用の手間なく、","必要な分だけ、","小さく始められます。")}</p>
    <p class="private">{W("本業に集中できると、","プライベートにも","ゆとりが生まれます。")}</p>
  </section>

  <!-- 04 できること -->
  <section class="has-before">
    <span class="num">04</span>
    <h2 class="r-h"><span class="mk"><em>できること</em>は、<br>大きく<em>3つ</em>。</span></h2>
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
      <p>{W("本格的なホームページ制作や","システム構築は、","専門の方に委託して進めます。")}{W("日常的な現場のお手伝いは、","たまになら喜んで。")}</p></details>
  </section>

  <!-- 05 ステップ -->
  <section class="gray">
    <span class="num">05</span>
    <h2 class="r-h"><span class="mk"><em>5つ</em>のステップで、<br><span class="wb">一緒に進めます。</span></span></h2>
    <ol class="steps">
      <li><div><b>相談する</b><span>頭の中を、そのまま話す</span></div></li>
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
    <p class="plan-note">{W("すべて税込・目安です。","内容や量に応じて、","ご相談のうえ決めます。")}</p>
    <p class="first">はじめての相談は <b>60</b>分無料</p>
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
        <div class="prof-top">{portrait}<div><b>クリエイティブサポーター</b><span>{W("接客販売15年、","印刷会社、","オンライン秘書")}</span></div></div>
        <p class="prof-msg">{W("「やりたい」が","いつも頭の中で大渋滞。")}{W("わたし自身がそんなタイプだから、","アイデアを抱える方の気持ちが","よくわかります。")}</p>
        <details class="more"><summary class="tri-only" aria-label="続きを読む"></summary>{more_body}</details>
      </div>
      <details class="more more-career"><summary>経歴・利用ツール</summary>{career}</details>
    </div>
  </section>

  <!-- 09 相談 -->
  <section class="purple" id="contact-r">
    <h2 class="r-h">その<em>「あれこれ」</em>、<br><span class="wb">聞かせてください。</span></h2>
    <p>まとまっていなくても大丈夫です。</p>
    <a class="btn btn-white" href="{FORM}" target="_blank" rel="noopener">相談フォームへ</a>
  </section>

{footer}
</div>
'''

js = script.replace(
    script[script.index("document.querySelectorAll(\n"):script.index(");", script.index("document.querySelectorAll(\n")) + 2],
    "document.querySelectorAll('#hero > *, .page > section > .r-h, .own, .nm-col, .strip, .bubbles li, .answer, .split > div, .gains li, .svc-card, .steps li, .plan, .spot, .names li, .prof-msg, #contact-r > p, #contact-r .btn');")

title = '<title>【見本】HITO IRO（ヒトイロ）｜あれこれサポート</title>'
head = re.sub(r'<title>.*?</title>', title, head)
head = head.replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1)
out = head + CSS + '</style>\n</head>\n<body>' + BODY + js + '\n</body>\n</html>\n'
open(os.path.join(ROOT, 'drafts/redesign.html'), 'w', encoding='utf-8').write(out)
print('書き出しました：drafts/redesign.html', len(out))
