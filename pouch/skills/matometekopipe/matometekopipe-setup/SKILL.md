---
name: matometekopipe-setup
description: 「まとめてCOPIPE」（Googleマップの保存リストから2〜3件選んでLINE用にコピーするWebアプリ）を、自分の Cloudflare に立てる・新しい版に入れかえる。「まとめてCOPIPEを立てたい」「自分用に公開したい」「まとめてCOPIPEを新しくしたい」と言われたときに使う。Cloudflare のアカウント作成やログインがまだなら、先に cloudflare-setup スキルを使う。
---

# まとめてCOPIPE を自分の Cloudflare に立てる

まとめてCOPIPE のコード一式（`src/` `public/` `migrations/` `wrangler.jsonc` `package.json` があるフォルダ）を、使う人の Cloudflare（無料プランで足ります）に公開するための手順です。返事はいつも日本語で、ですます・やわらかめの言葉で話してください。

## このファイルの置き方（使う人向け）

1. このファイルを `~/.claude/skills/matometekopipe-setup/SKILL.md` という名前で置きます（フォルダがなければ作ります）。
2. いっしょに配っている `cloudflare-setup.md` も、`~/.claude/skills/cloudflare-setup/SKILL.md` に置きます。
3. まとめてCOPIPE のコードのフォルダで Claude Code を開き、「まとめてCOPIPEを立てたい」と話しかけます。

## 守ること

- **Cloudflare のアカウント作成、ログイン、支払いの設定は、本人がします。** パスワードやカード番号を聞いたり、代わりに入れたりしません。`npx wrangler login` のあとにブラウザで「許可」を押すのも本人です。
- **すでにある Worker やデータベースを上書きしたり、消したりしません。** 公開する前に、同じ名前の Worker がないか確かめます（下の 3）。
- 秘密の値（APIキーなど）は使いません。まとめてCOPIPE には、いりません。
- コードの中の Googleマップの読み出し口は、Google の正式なものではありません。急に読めなくなることがある、と最初に伝えます。

## 手順

### 1. 準備ができているか確かめる

```sh
node -v                 # 18 以上ならよい
npx wrangler whoami     # ログインしているアカウントが出る
```

- `node` がなければ、https://nodejs.org から LTS 版を入れてもらいます（本人の作業）。
- `wrangler whoami` でログインしていなければ、**cloudflare-setup スキル**の手順に切りかえます。
- アカウントがいくつも出たときは、どれに立てるか本人に聞きます。

コードのフォルダで、部品を入れます。

```sh
npm install
```

### 2. 形を決める（本人に聞く）

次の2つは、本人に聞いてから決めます。

- **Worker の名前**：アドレスは `https://<名前>.<アカウントのサブドメイン>.workers.dev` になります。英小文字・数字・ハイフンだけです。とくに希望がなければ `matometekopipe` にします。
- **使い方**
  - **ひとり用（ふつうはこちら）**：家族など、アドレスを知っている人は誰でも同じリストを見たり消したりできます。アドレスは広めないように伝えます。
  - **みんなに配る用**：開いた人ごとに「自分用のアドレス」（`/u/長い英数字`）ができ、リストが人ごとに分かれます。`MULTI` を `"1"` にします。

### 3. 同じ名前の Worker がないか確かめる

```sh
npx wrangler deployments list --name <名前>
```

もう公開した記録が出たら、その名前は使わずに、本人に別の名前を決めてもらいます（上書きすると、前のアプリが消えてしまうため）。「見つからない」という意味のエラーなら、使ってよい名前です。

### 4. データベース（D1）を作る

```sh
npx wrangler d1 create <名前>-db
```

出てきた `database_id` を控えます。

### 5. wrangler.jsonc を、その人用に書きかえる

配られた `wrangler.jsonc` には、作者の Worker 名とデータベースのIDが入っています。次のように直します。

- `"name"` → 2 で決めた名前
- `d1_databases` の `"database_name"` → `<名前>-db`、`"database_id"` → 4 で控えたID（`"binding": "DB"` と `"migrations_dir": "migrations"` はそのまま）
- `"env"` の中の `"share"`（作者の配布用の設定）は、まるごと消します。
- **みんなに配る用**にするときだけ、いちばん外側に `"vars": { "MULTI": "1" }` を足します。

`package.json` の `db:migrate`・`deploy` などは作者の2つのアドレス向けなので、使いません。下のコマンドを直接使います。

### 6. 表を作って、公開する

```sh
npx wrangler d1 migrations apply <名前>-db --remote
npx wrangler deploy
```

はじめて公開するアカウントでは、`workers.dev` のサブドメインを決めるよう聞かれることがあります。そのときは **cloudflare-setup スキル**の「workers.dev のサブドメイン」のとおりに進めます。

### 7. 動くか確かめる

```sh
curl -s https://<名前>.<サブドメイン>.workers.dev/api/state
```

- ひとり用：`{"lists":[],"mine":[],"pending":0,"multi":false}` のように出れば成功です。
- みんなに配る用：`{"needKey":true}` と出れば成功です。

最後に、アドレスを本人に伝え、次のことを案内します。

- iPhone は Safari で開いて、共有ボタン →「ホーム画面に追加」。Android は Chrome の「︙」→「ホーム画面に追加」。
- みんなに配る用は、「自分用のアドレスを作る」を押して `/u/…` のページになってから、ホーム画面に追加します。そのアドレスをなくすと、自分のリストに戻れません。
- リストは、Googleマップの共有で「リンクを知っている人」が見られる形にします。
- Googleが混み合っていると（429）、登録したばかりのリストは少し待つことがあります。

## 新しい版に入れかえるとき

1. 新しいコード一式を受け取り、5 で直した `wrangler.jsonc` は**自分の分を残します**（上書きしない）。
2. 次のコマンドで入れかえます。

```sh
npm install
npx wrangler d1 migrations apply <名前>-db --remote   # 表の変更があれば当たる。なければ「適用するものはない」と出る
npx wrangler deploy
```

3. 7 と同じように確かめます。

## うまくいかないとき

- **リストが読めない**：リストの共有が「リンクを知っている人」になっているか確かめます。
- **「混み合っています」と出る**：Google が Cloudflare からの読み出しを断っています（429）。時間をおいてリロードマークを押します。
- **ずっと読めない**：Google 側が変わった可能性があります。`npx wrangler tail <名前>` で、ログに `getlist failed` が出ていないか見ます。配った人（作者）に知らせます。
- **Cloudflare のエラー（ログイン・権限・サブドメインなど）**：cloudflare-setup スキルの「よくあるエラー」を見ます。
