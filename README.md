# HITO IRO（あれこれサポート）紹介ページ

名刺・ポストカードのQRから来た人に、「どんなことを頼めるサービスか」を伝える1ページのサイトです。

- 公開URL： https://life.aokoworks.workers.dev
- 置き場所： Cloudflare Workers（`life` という名前のWorker）

## ファイルの見取り図

```
public/
  index.html           ← ページ本体。色・画像もすべてこの1枚に入っている
  movie.html           ← 紹介動画だけのページ（動画・ポスター・アイコンも public/ に入っている）
  pouch/               ← 自作の道具を配る「my pouch」（自動で作られるページ）
pouch/
  tools.json           ← my pouch の道具のデータ。道具を足すときはここを直す
  README.md            ← my pouch の足し方メモ
design/
  form-header.png      ← Googleフォームのヘッダー画像（サイトには載せない）
wrangler.jsonc         ← 公開するときの設定。Worker名 life は変更しないこと

（以前の自作フォーム用で、今は使っていないもの）
src/worker.js, public/style.css, public/thanks.html, public/sorry.html, SETUP.md
```

## よくある書き換え

| やりたいこと | 直す場所 |
|---|---|
| 文章を直す | `public/index.html` |
| 色を変える | `public/index.html` の一番上、`:root` の色 |
| 相談フォームのリンク先を変える | `public/index.html` の `forms.gle` の3か所 |

## 公開のしかた（今のやり方）

1. `public` フォルダを、中身を全部そろえたままパソコンに用意する
2. Cloudflare の管理画面で Worker `life` を開き、右上の「新規展開」を押す
3. `public` フォルダの中身を全部ドラッグして「デプロイ」を押す
4. https://life.aokoworks.workers.dev を開いて確認する

新規展開は、アップロードしたファイルでサイト全体を入れ替えます。1つでも抜けると、そのファイルはサイトから消えるので、必ず全部まとめてアップロードしてください。

## パソコンで見た目を確かめる

`public/index.html` をダブルクリックすると、ブラウザで開けます。公開前の確認はこれで十分です。

## 以前の自作フォームについて

相談は今、Googleフォームで受けています。以前作ったメール通知つきのフォーム（`src/worker.js`）は使っていません。
もう一度使う場合の手順は [SETUP.md](SETUP.md) に残してあります。
