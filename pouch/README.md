# my pouch の足し方メモ

my pouch は、自作の道具を配るページです。

- 一覧ページ：https://life.aokoworks.workers.dev/pouch/
- 道具のページ：https://life.aokoworks.workers.dev/pouch/（英字の名前）/

道具の情報は、すべて **`pouch/tools.json`** の1つのファイルにまとめてあります。
ページ（`public/pouch/` の中の html）は、このファイルから自動で作っています。html を手で直すと、次に作り直したときに消えるので、直すときは必ず `tools.json` を直します。

Claude に頼むときは「my pouch に〇〇を足して」と言えば、この手順で進めます。

## 0. Claude への頼み方（いちばんかんたんな方法）

新しいセッションを始めるとき、リポジトリは **`aoko-life`** を選びます。そのうえで、次の見本をコピーして、〇〇を埋めて送ります。
ファイル（zip や画像）は、メッセージにそのまま添付します。

**道具を新しく足すとき**
```
my pouch に道具を足して
・名前：〇〇
・つまり：〇〇（1行）
・説明：〇〇（2〜3文）
・アプリのURL：〇〇（なければ「なし」）
・スキルのzip：添付（まだなら「準備中」）
・画像：添付（なければ「なし」）
・noteの記事：タイトル／URL（なければ「なし」）
・載せる日：〇月〇日
```

**あとからスキルのzipを入れるとき**
```
my pouch の〇〇（道具の名前）に、スキルのzipを入れて（zipを添付）
```

**あとから note の記事を足すとき**
```
my pouch の〇〇（道具の名前）に、noteの記事を足して
タイトル：〇〇
URL：〇〇
```

**道具を一時的に隠すとき**
```
my pouch の〇〇を非公開にして
```

Claude は、データを直してページを作り直し、スマホで見た画面と、公開用の一式（zip）を返します。確認してOKなら、公開用の一式を Cloudflare にアップロードします（下の「4. 公開する」）。

## 1. 道具を1つ足す

`pouch/tools.json` の `[` のすぐ下に、次のかたまりを1つ足します（かたまりとかたまりの間は `,` で区切る）。

```json
  {
    "name": "道具の名前",
    "slug": "eiji-no-namae",
    "tsumari": "どんな小さな不便をほどくか（1行）",
    "summary": "一覧のカードに出す短い説明",
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
| `tsumari` | どんな小さな不便をほどくか（1行）。道具のページに出る | はい |
| `summary` | 一覧のカードに出す短い説明。空なら `tsumari` を出す | いいえ |
| `description` | 何ができるか（2〜3文） | はい |
| `image` | カードとページの上に出す画像 | いいえ |
| `app_url` | すぐ使える配布用アプリのURL | いいえ |
| `skill_zip` | ダウンロードさせるスキルのzip | いいえ |
| `tools` | 対応しているツール | いいえ |
| `notes` | noteの記事（タイトルとURL。いくつでも） | いいえ |
| `date` | 載せた日。新しい日付ほど一覧の上に来る | はい |
| `published` | `true` で公開、`false` で隠す（準備中の道具用） | はい |

- 使わない項目は `""`（空）や `[]`（空のリスト）にすれば、ページには出ません
- 文の途中に `|` を入れると、スマホでそこから折り返しやすくなります（`|` 自体はページに出ません）。例：`"Googleマップから|保存情報を共有したいときに、…"`
- `skill_zip` が空、またはファイルがまだ置かれていないときは、ボタンが「スキルは準備中です」になります（壊れたリンクにはなりません）
- `image` も、ファイルがまだ置かれていなければ表示されません

## 2. スキルと画像を置く場所

**スキル**は、`pouch/skills/（英字の名前）/` のフォルダに、配りたいファイルをそのまま入れます。
`python3 pouch/build.py` を実行すると、自動で zip にまとめて `public/pouch/files/（英字の名前）-skills.zip` に置き、ダウンロードボタンにつなぎます（`skill_zip` は空のままでよい）。

```
pouch/skills/matometekopipe/
  はじめにお読みください.txt
  matometekopipe-setup/SKILL.md
  cloudflare-setup/SKILL.md
```

- できあがった zip を自分で置きたいときは、`public/pouch/files/` に入れて `"skill_zip": "pouch/files/〇〇.zip"` と書きます
- ページに出す「使い方の3ステップ」は、`"skill_steps": ["1つめ", "2つめ", "3つめ"]` で道具ごとに変えられます。書かなければ、いつもの3ステップが出ます
- ステップの下に出す補足は `"skill_note": ["1行目", "2行目"]` に書きます（1つずつ改行して出ます。なければ出ません）

**画像**は `public/pouch/images/` に置き、`"image": "pouch/images/〇〇.jpg"` と書きます。横幅 800px くらい・200KB 以下にしておくと、スマホでも軽く開けます。

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
  skills/〇〇/      ← 配るスキルの元のファイル
public/pouch/
  index.html        ← 一覧ページ（自動で作られる）
  〇〇/index.html   ← 道具ごとのページ（自動で作られる）
  mypouch-icon.png  ← 一覧ページのアイコン
  mypouch-icon-64.png ← トップページの入口の小さいアイコン
  hitoiro-logo.webp ← my pouch の上と下に出す HITO IRO のロゴ
  og.png            ← リンクを貼ったときに出るカード画像（道具の画像がないとき）
  files/            ← スキルのzip（pouch/skills/ から自動で作られる）
  images/           ← 道具の画像
```
