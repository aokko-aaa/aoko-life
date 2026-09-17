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
wrangler.jsonc         ← 公開するときの設定。Worker名 life は変更しないこと
```

## よくある書き換え

| やりたいこと | 直す場所 |
|---|---|
| 連絡先を決める | `public/index.html` の `<!-- TODO: 連絡先 -->` の下のリンク1か所 |
| 文章を直す | `public/index.html` |
| 作例画像を入れる・差し替える | `public/images/` に同じ名前で置く |
| 色を変える | `public/style.css` の一番上、`:root` の3色 |

## パソコンで見た目を確かめる

`public/index.html` をダブルクリックすると、ブラウザで開けます。公開前の確認はこれで十分です。

## 公開する

ターミナルでこのフォルダに入って、次の1行です（Cloudflareへのログインが必要です）。

```
npx wrangler deploy
```

終わったら https://life.aokoworks.workers.dev を開いて、表示を確認します。
