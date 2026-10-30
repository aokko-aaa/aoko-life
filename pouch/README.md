# my pouch の足し方メモ

my pouch は、自作の道具を配るページです。

- 一覧ページ：https://life.aokoworks.workers.dev/pouch/
- 道具のページ：https://life.aokoworks.workers.dev/pouch/（英字の名前）/

道具の情報は、すべて **`pouch/tools.json`** の1つのファイルにまとめてあります。
ページ（`public/pouch/` の中の html）は、このファイルから自動で作っています。html を手で直すと、次に作り直したときに消えるので、直すときは必ず `tools.json` を直します。

Claude に頼むときは「my pouch に〇〇を足して」と言えば、この手順で進めます。

## 1. 道具を1つ足す

`pouch/tools.json` の `[` のすぐ下に、次のかたまりを1つ足します（かたまりとかたまりの間は `,` で区切る）。

```json
  {
    "name": "道具の名前",
    "slug": "eiji-no-namae",
    "tsumari": "どんな小さな不便をほどくか（1行）",
    "description": "何ができるか（2〜3文）",
    "image": "pouch/images/eiji-no-namae.jpg",
    "app_url": "https://〇〇.aokoworks.workers.dev",
    "skill_zip": "pouch/files/eiji-no-namae.zip",
    "tools": ["Claude Code", "Codex"],
    "notes": [
      {"title": "noteの記事のタイトル", "url": "https://note.com/aokoworks/n/〇〇"}
    ],
    "date": "2026-11-01",
    "published": true
  },
```

| 項目 | 中身 | 必須 |
|---|---|---|
| `name` | 道具の名前 | はい |
| `slug` | ページのアドレスの英字（/pouch/〇〇/ の〇〇）。英小文字・数字・ハイフンだけ | はい |
| `tsumari` | どんな小さな不便をほどくか（1行） | はい |
| `description` | 何ができるか（2〜3文） | はい |
| `image` | カードとページの上に出す画像 | いいえ |
| `app_url` | すぐ使える配布用アプリのURL | いいえ |
| `skill_zip` | ダウンロードさせるスキルのzip | いいえ |
| `tools` | 対応しているツール | いいえ |
| `notes` | noteの記事（タイトルとURL。いくつでも） | いいえ |
| `date` | 載せた日。新しい日付ほど一覧の上に来る | はい |
| `published` | `true` で公開、`false` で隠す（準備中の道具用） | はい |

- 使わない項目は `""`（空）や `[]`（空のリスト）にすれば、ページには出ません
- `skill_zip` が空、またはファイルがまだ置かれていないときは、ボタンが「スキルは準備中です」になります（壊れたリンクにはなりません）
- `image` も、ファイルがまだ置かれていなければ表示されません

## 2. スキルのzipと画像を置く場所

| もの | 置く場所 | tools.json での書き方 |
|---|---|---|
| スキルのzip | `public/pouch/files/` | `"skill_zip": "pouch/files/〇〇.zip"` |
| 画像 | `public/pouch/images/` | `"image": "pouch/images/〇〇.jpg"` |

- スキルは、フォルダごと zip にしてから置きます
- 画像は横幅 800px くらい・200KB 以下にしておくと、スマホでも軽く開けます

## 3. ページを作り直す

リポジトリの一番上で、次を実行します。

```
python3 pouch/build.py
```

`書き出しました：一覧と道具 〇 件` と出れば完了です。
（`pip install budoux` を入れておくと、日本語の改行がよりきれいになります）

## 4. 公開する

1. `public` フォルダを、フォルダごとパソコンに用意する（中身を全部そろえたまま）
2. Cloudflare の管理画面で Worker `life` を開き、右上の「新規展開」を押す
3. `public` フォルダの**中身全部**をドラッグして「デプロイ」を押す
4. https://life.aokoworks.workers.dev/pouch/ を開いて確認する

**注意：** 新規展開は、アップロードしたファイルでサイト全体を入れ替えます。1つでも抜けると、そのファイルはサイトから消えます。必ず `public` の中身を全部まとめてアップロードしてください。

## 5. noteの記事をあとから足す

`pouch/tools.json` の、その道具の `"notes"` に1行足して、3 と 4 をやり直します。

```json
    "notes": [
      {"title": "1本目のタイトル", "url": "https://note.com/aokoworks/n/〇〇"},
      {"title": "2本目のタイトル", "url": "https://note.com/aokoworks/n/〇〇"},
      {"title": "足したい記事のタイトル", "url": "https://note.com/aokoworks/n/〇〇"}
    ],
```

最後の行のあとには `,` を付けません。

## ファイルの一覧

```
pouch/
  tools.json        ← 道具のデータ（ここだけ直す）
  build.py          ← ページを作る仕組み
  README.md         ← このメモ
public/pouch/
  index.html        ← 一覧ページ（自動で作られる）
  〇〇/index.html   ← 道具ごとのページ（自動で作られる）
  mypouch-icon.png  ← 一覧ページのアイコン
  mypouch-icon-64.png ← トップページの入口の小さいアイコン
  og.png            ← リンクを貼ったときに出るカード画像（道具の画像がないとき）
  files/            ← スキルのzip
  images/           ← 道具の画像
```
