---
name: cloudflare-setup
description: Cloudflare Workers + D1 のアプリを公開できるように、Cloudflare のアカウント・wrangler のログイン・workers.dev のサブドメイン・D1 を整える。「Cloudflareの設定をしたい」「wrangler にログインしたい」「Cloudflareに公開できない」と言われたとき、または matometekopipe-setup などの公開手順の途中でログインやアカウントが必要になったときに使う。
---

# Cloudflare の設定（Workers + D1）

Cloudflare Workers と D1（データベース）を使うアプリを、使う人の Cloudflare に公開できる状態にします。返事はいつも日本語で、ですます・やわらかめの言葉で話してください。はじめての人向けに、1つずつ確かめながら進めます。

## このファイルの置き方（使う人向け）

このファイルを `~/.claude/skills/cloudflare-setup/SKILL.md` という名前で置きます（フォルダがなければ作ります）。

## 守ること

- **アカウント作成・ログイン・メールの確認・支払いの設定は、本人がします。** パスワード、カード番号、APIトークンを聞いたり、代わりに入れたりしません。
- **秘密の値は、本人が入れます。** アプリに秘密の値がいるときは、本人に `npx wrangler secret put <名前>` を打ってもらいます。値をチャットに貼ってもらったり、ファイルに書いたりしません。
- **すでにある Worker・データベース・ドメインを、消したり上書きしたりしません。** 同じ名前があったら、本人に別の名前を決めてもらいます。
- 無料プランで足りるかどうかは、Cloudflare の料金ページ（https://www.cloudflare.com/plans/developer-platform/ ）で本人に確かめてもらいます。数字を覚えで言い切りません。

## 1. アカウント

`npx wrangler whoami` を打って、ログインしているか確かめます。

- ログインしていて、使いたいアカウントが出る → 3 へ進みます。
- アカウントがない → 本人に https://dash.cloudflare.com/sign-up で作ってもらいます。届いたメールの確認も済ませてもらいます。

## 2. wrangler のログイン

アプリのフォルダで：

```sh
npm install            # package.json に wrangler が入っていれば、これで入る
npx wrangler login
```

ブラウザが開くので、本人に Cloudflare にログインして「Allow（許可）」を押してもらいます。終わったら、もう一度 `npx wrangler whoami` で確かめます。

- アカウントがいくつも出たときは、どれを使うか本人に聞きます。そのアカウントIDを `wrangler.jsonc` の `"account_id"` に書くと、毎回聞かれなくなります。
- ブラウザが開けない環境では、ログインはできません。本人のパソコンで打ってもらいます。

## 3. workers.dev のサブドメイン

Worker は `https://<Worker名>.<サブドメイン>.workers.dev` で公開されます。サブドメインはアカウントに1つだけです。

- はじめての `npx wrangler deploy` で、サブドメインを決めるよう聞かれることがあります。本人に名前を決めてもらって答えます。
- 聞かれないまま公開に失敗したときは、本人に Cloudflare のダッシュボード → 「Workers & Pages」を開いてもらいます。サブドメインの設定がそこにあります。
- サブドメインはあとから変えられますが、変えるとホーム画面に追加したアドレスが使えなくなります。最初によく考えて決めてもらいます。

## 4. D1（データベース）

```sh
npx wrangler d1 list                          # すでにあるデータベース
npx wrangler d1 create <データベース名>        # 新しく作る（同じ名前があれば作らない）
```

`create` で出た `database_id` を、`wrangler.jsonc` の `d1_databases` に書きます。`binding` は、アプリのコードが使う名前（例：`DB`）のままにします。

表を作る・変えるのは、migrations フォルダの SQL を当てるときです。

```sh
npx wrangler d1 migrations apply <データベース名> --local    # 手元で試す
npx wrangler d1 migrations apply <データベース名> --remote   # 本番
```

migrations の SQL は、すでに当てたファイルを書きかえずに、新しい番号のファイルを足します。

## 5. 公開と確かめ

```sh
npx wrangler deployments list --name <Worker名>   # 同じ名前がないか、先に確かめる
npx wrangler deploy
npx wrangler tail <Worker名>                      # 動いている間のログを見る（Ctrl+C で止める）
```

公開したら、表示されたアドレスを開いて（または `curl` で）動くか確かめ、本人に伝えます。

## よくあるエラー

- **`Authentication error` / `not logged in`**：ログインが切れています。2 をやり直します。
- **`You need to register a workers.dev subdomain`**：3 を見ます。
- **`A worker with this name already exists`／前のアプリが変わってしまった**：同じ名前に上書きしています。すぐ本人に知らせて、名前を変えて公開し直します。前の版は、ダッシュボードの Worker →「Deployments」から本人に戻してもらえます。
- **`D1_ERROR: no such table`**：表を作っていません。4 の `migrations apply --remote` を打ちます。
- **`database_id` がちがう／見つからない**：`npx wrangler d1 list` の ID と `wrangler.jsonc` を見比べます。
- **アカウントがちがう**：`npx wrangler whoami` で確かめ、`wrangler.jsonc` の `"account_id"` を直します。
- **外のサイトから `429`（多すぎ）と断られる**：Cloudflare からの読み出しを相手が断っています。時間をおきます。設定では直りません。
