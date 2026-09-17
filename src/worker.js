/**
 * フォームの受付係。
 *
 * ・/api/contact に送信が来たら、内容をLINEに送る
 * ・それ以外のアクセスは、public/ の中のファイルをそのまま返す
 *
 * 必要な鍵（コードには書かない。wrangler secret put で預ける）
 *   LINE_CHANNEL_ACCESS_TOKEN … LINE公式アカウントを操作するための合言葉
 *   LINE_USER_ID              … 送り先（あおこさん自身）のID
 */

const LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push";

// 入力の上限。長すぎるものは切って送る
const LIMIT = { name: 100, email: 200, body: 1500 };

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/contact") {
      if (request.method !== "POST") {
        return Response.redirect(new URL("/#contact", url).toString(), 303);
      }
      return handleContact(request, env, url);
    }

    // フォーム以外は、置いてあるファイルをそのまま返す
    return env.ASSETS.fetch(request);
  },
};

async function handleContact(request, env, url) {
  const seeOther = (path) => Response.redirect(new URL(path, url).toString(), 303);

  let form;
  try {
    form = await request.formData();
  } catch {
    return seeOther("/sorry");
  }

  // 自動送信よけ。人には見えない欄で、埋まっていたら機械とみなす
  if ((form.get("company") || "").trim() !== "") {
    // 送ったつもりで終わらせる（相手に対策を気づかせない）
    return seeOther("/thanks");
  }

  const name = cut(form.get("name"), LIMIT.name);
  const email = cut(form.get("email"), LIMIT.email);
  const body = cut(form.get("body"), LIMIT.body);

  if (!name || !email || !body) {
    return seeOther("/sorry");
  }

  const text =
    "サイトからお問い合わせが届きました\n" +
    "----------------\n" +
    `お名前： ${name}\n` +
    `メール： ${email}\n` +
    "----------------\n" +
    body;

  const ok = await pushToLine(env, text);
  return seeOther(ok ? "/thanks" : "/sorry");
}

async function pushToLine(env, text) {
  if (!env.LINE_CHANNEL_ACCESS_TOKEN || !env.LINE_USER_ID) {
    console.error("LINEの鍵が設定されていません");
    return false;
  }

  try {
    const res = await fetch(LINE_PUSH_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${env.LINE_CHANNEL_ACCESS_TOKEN}`,
      },
      body: JSON.stringify({
        to: env.LINE_USER_ID,
        messages: [{ type: "text", text }],
      }),
    });

    if (!res.ok) {
      console.error("LINEに送れませんでした", res.status, await res.text());
      return false;
    }
    return true;
  } catch (err) {
    console.error("LINEへの接続に失敗しました", err);
    return false;
  }
}

function cut(value, max) {
  const s = String(value ?? "").trim();
  return s.length > max ? s.slice(0, max) + "…（以下省略）" : s;
}
