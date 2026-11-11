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
  .purple .num{color:var(--accent);}

  /* 見出し：キーワードだけ大きく紫、つなぎは小さく */
  .r-h{font-size:19px;font-weight:700;line-height:1.4;margin-bottom:28px;letter-spacing:.02em;}
  .r-h em{font-style:normal;font-size:28px;color:var(--brand);}
  .purple .r-h em{color:var(--paper);background:linear-gradient(transparent 78%,rgba(180,255,63,.9) 78%);}
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
  .r-label{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.16em;color:var(--brand);background:var(--accent);border-radius:999px;padding:0 12px;line-height:1.8;margin-bottom:16px;}
  .ask{font-size:17px;font-weight:700;line-height:1.6;margin-bottom:28px;}
  .ask small{display:block;font-size:14px;font-weight:400;line-height:1.8;margin-top:8px;opacity:.9;}
  .split{display:grid;gap:10px;}
  .split > div{border-radius:20px;padding:20px;}
  .split .you{border:2px solid rgba(255,255,255,.55);}
  .split .us{background:var(--paper);color:var(--ink);}
  .split p{font-weight:700;line-height:1.6;margin-bottom:10px;}
  .split .us p{color:var(--brand);}
  .split li{display:inline-block;font-size:13px;font-weight:700;line-height:1.6;border-radius:999px;padding:4px 12px;margin:0 4px 6px 0;background:rgba(255,255,255,.16);}
  .split .us li{background:var(--soft-purple);color:var(--brand);}
  .gains{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:28px;}
  .gains li{background:var(--paper);color:var(--ink);border-radius:16px;padding:16px 6px 14px;text-align:center;font-size:12px;font-weight:700;line-height:1.6;}
  .gains svg{width:36px;height:36px;color:var(--brand);display:block;margin:0 auto 6px;}
  .chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:20px;}
  .chips li{font-size:13px;font-weight:700;border:1px solid rgba(255,255,255,.6);border-radius:999px;padding:4px 12px;line-height:1.6;}
  .private{margin-top:20px;font-size:13px;line-height:1.8;opacity:.9;}

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
  .trial-r{margin-top:12px;background:var(--accent);color:var(--ink);border-radius:999px;text-align:center;font-weight:700;line-height:1.6;padding:10px 12px;font-size:14px;}
  .spot{background:var(--paper);color:var(--ink);border-radius:24px;padding:20px;margin-top:10px;}
  .spot > p{font-weight:700;color:var(--brand);margin-bottom:6px;}
  .spot li{display:flex;justify-content:space-between;gap:12px;align-items:baseline;padding:10px 0;border-bottom:1px dashed var(--line);font-size:14px;line-height:1.6;}
  .spot li:last-child{border-bottom:0;}
  .spot li b{color:var(--brand);white-space:nowrap;}
  .first{margin-top:16px;text-align:center;font-weight:700;line-height:1.6;}
  .first b{font-size:30px;}

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
    .split{grid-template-columns:1fr 1fr;gap:16px;}
    .gains{gap:16px;}
    .gains li{font-size:15px;padding:28px 12px;}
    .gains svg{width:48px;height:48px;}
    .svc{grid-template-columns:repeat(3,1fr);gap:16px;}
    .ways-r{max-width:640px;}
    .steps{grid-template-columns:repeat(5,1fr);}
    .steps li{grid-template-columns:1fr;justify-items:center;text-align:center;padding:24px 12px;}
    .plans-r{grid-template-columns:1fr 1fr;gap:16px;}
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
    <div class="badges">
      <div><small>はじめての相談</small><b>60</b><span>分無料</span></div>
      <div><small>月額</small><b>6</b><span>万円〜</span></div>
      <div><small>スポット</small><b>5,000</b><span>円〜</span></div>
    </div>
  </section>

  <!-- 02 お悩み -->
  <section class="gray">
    <span class="num">02</span>
    <h2 class="r-h">その<em>「あれこれ」</em>、<br>ひとりで<em>抱えて</em><span class="wb">いませんか？</span></h2>
    <ul class="bubbles">
      <li>{W("何から始めよう…")}</li>
      <li>{W("考えが、","形にならない")}</li>
      <li>{W("雑用で、","本業が後回しに")}</li>
      <li>{W("人を増やすのは、","ためらう")}</li>
      <li>{W("ちょっと","相談したい")}</li>
      <li>{W("AIを使いたいけど…")}</li>
    </ul>
    <div class="answer"><p>{W("ひとりで抱えなくて、","大丈夫です！")}</p></div>
  </section>

  <!-- 03 思い -->
  <section class="purple">
    <span class="r-label">HITO IROの思い</span>
    <h2 class="r-h"><em>あなたにしか</em><br><span class="wb">できない仕事に、</span><br><em>あなたの時間</em>を。</h2>
    <p class="ask">{W("お客さまが待っているのは、","あなたです。")}<small>{W("請求書や調べものを","あなたがやったから","喜ぶお客さまは、","いるでしょうか。")}</small></p>
    <div class="split">
      <div class="you"><p>あなたが向き合うこと</p><ul><li>お客さまとの対話</li><li>商品・サービスづくり</li><li>次の一手を決めること</li></ul></div>
      <div class="us"><p>ヒトイロに任せること</p><ul><li>請求書・事務作業</li><li>リサーチ・資料づくり</li><li>SNS・販促の準備</li><li>進み具合の管理</li></ul></div>
    </div>
    <ul class="gains">
      <li>{talk}{W("信頼が","深まる")}</li>
      <li>{spark}{W("新しい企画が","動く")}</li>
      <li>{arrow}{W("事業が","前へ進む")}</li>
    </ul>
    <ul class="chips"><li>採用の手間なし</li><li>必要な分だけ</li><li>小さく始められる</li></ul>
    <p class="private">{W("本業に集中できると、","プライベートにも","ゆとりが生まれます。")}</p>
  </section>

  <!-- 04 できること -->
  <section class="has-before">
    <span class="num">04</span>
    <h2 class="r-h"><em>できること</em>は、<br>大きく<em>3つ</em>。</h2>
    <p class="motto-r">効率はAIで。彩りは人で。</p>
    <div class="svc">
      <div class="svc-card"><h3><i>A</i>頭の中の「あれこれ」</h3>
        <ul class="tags"><li>壁打ち・相談</li><li>アイデアの言語化</li><li>優先順位の整理</li><li>やることリスト化</li></ul></div>
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
    <h2 class="r-h"><em>5つ</em>のステップで、<br><span class="wb">一緒に進めます。</span></h2>
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
    <div class="plans-r">
      <div class="plan"><p>スタンダード</p><p class="price"><b>6</b><span>万円/月</span></p><small>思考の整理から実務まで、まるごと</small></div>
      <div class="plan"><p>フルサポート</p><p class="price"><b>9</b><span>万円/月</span></p><small>{W("現場でのお手伝いも。","（西三河/名古屋方面のみ）")}</small></div>
    </div>
    <p class="trial-r">{W("はじめての方は、","1ヶ月だけ3.5万円で","お試しOK（1回限り）")}</p>
    <div class="spot"><p>スポット（これだけ頼みたい）</p>
      <ul>
        <li><span>リサーチ・比較資料</span><b>1万5,000円〜</b></li>
        <li><span>販促物の作成（印刷費別）</span><b>1万円〜</b></li>
        <li><span>イラスト制作</span><b>5,000円〜</b></li>
        <li><span>SNS運用サポート</span><b>3万5,000円〜</b></li>
        <li><span>AI使い方相談（1対1）</span><b>1時間5,000円〜</b></li>
      </ul>
    </div>
    <p class="first">はじめての相談は <b>60</b>分無料</p>
  </section>

  <!-- 07 名前 -->
  <section>
    <span class="num">07</span>
    <h2 class="r-h"><em>HITO IRO</em>という名前</h2>
    <ul class="names">
      <li><b>人 × 色</b><span>{W("それぞれの個性を","大切に")}</span></li>
      <li><b><span class="wb">ひとり ×</span><span class="wb">ひといろ</span></b><span>{W("新しい視点と","彩りを")}</span></li>
      <li><b>人の温度</b><span>{W("AIを使っても、","温かさは失わない")}</span></li>
      <li><b>彩る</b><span>{W("塗り替えずに、","一色を添える")}</span></li>
    </ul>
    <p class="names-close">{W("事業の色を塗り替えない。","もうひといろを添える。")}</p>
  </section>

  <!-- 08 プロフィール -->
  <section class="gray" id="profile-r">
    <span class="num">08</span>
    <h2 class="r-h"><em>プロフィール</em></h2>
    <div class="prof-wrap">
      <div>
        <div class="prof-top">{portrait}<div><b>クリエイティブサポーター</b><span>{W("接客販売15年、","印刷会社、","オンライン秘書")}</span></div></div>
        <p class="prof-msg">{W("「やりたい」が","いつも頭の中で大渋滞。")}{W("わたし自身がそんなタイプだから、","アイデアを抱える方の気持ちが","よくわかります。")}</p>
        <details class="more"><summary><span class="more-open">続きを読む</span><span class="more-close">閉じる</span></summary>{more_body}</details>
      </div>
      <details class="more more-career"><summary><span class="more-open">経歴・利用ツールを見る</span><span class="more-close">閉じる</span></summary>{career}</details>
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
    "document.querySelectorAll('#hero > *, .page > section > .r-h, .bubbles li, .answer, .split > div, .gains li, .svc-card, .steps li, .plan, .spot, .names li, .prof-msg, #contact-r > p, #contact-r .btn');")

title = '<title>【見本】HITO IRO（ヒトイロ）｜あれこれサポート</title>'
head = re.sub(r'<title>.*?</title>', title, head)
head = head.replace('<head>', '<head>\n<meta name="robots" content="noindex">', 1)
out = head + CSS + '</style>\n</head>\n<body>' + BODY + js + '\n</body>\n</html>\n'
open(os.path.join(ROOT, 'drafts/redesign.html'), 'w', encoding='utf-8').write(out)
print('書き出しました：drafts/redesign.html', len(out))
