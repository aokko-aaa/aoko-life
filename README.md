# あおこ 紹介ページ

名刺・ポストカードのQRから来た人に、「なにを頼める人か」を伝える1ページのサイトです。

- 公開URL： https://life.aokoworks.workers.dev
- 置き場所： Cloudflare Workers（`life` という名前のWorker）

## ファイルの見取り図

```
public/                ← ここに入っているものが、そのままサイトになる
  index.html           ← 文章とページの中身
  style.css            ← 色や文字の大きさ
  images/              ← 作例画像（work-01.jpg / work-02.jpg）
src/worker.js          ← フォームの受付係
wrangler.jsonc         ← 公開するときの設定。Worker名 life は変更しないこと
SETUP.md               ← フォームを動かすまでの手順
```

## よくある書き換え

| やりたいこと | 直す場所 |
|---|---|
| 届く先のメールアドレスを変える | `npx wrangler secret put MAIL_TO` をやり直す |
| 文章を直す | `public/index.html` |
| 作例画像を入れる・差し替える | `public/images/` に同じ名前で置く |
| 色を変える | `public/style.css` の一番上、`:root` の3色 |

## パソコンで見た目を確かめる

`public/index.html` をダブルクリックすると、ブラウザで開けます。公開前の確認はこれで十分です。

## お問い合わせフォームの設定と、公開のしかた

**[SETUP.md](SETUP.md) に、上から順にやることを書いてあります。** 初回はそちらを見てください。

2回目以降、文章や画像を直して公開し直すときは、この2行だけです。

```
git pull
npx wrangler deploy
```

終わったら https://life.aokoworks.workers.dev を開いて、表示を確認します。

## フォームが届く仕組み

```
訪問者がフォームを送る
   ↓
src/worker.js（受付係）が受け取る
   ↓
あおこさんのメールに届く ＋（設定すれば）LINEにも届く
   ↓
そのメールに返信すると、相談者に返る
```
