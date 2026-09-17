/**
 * フォームの受付係。
 *
 * ・/api/contact に送信が来たら、内容をメール（と、設定していればLINE）で知らせる
 * ・それ以外のアクセスは、public/ の中のファイルをそのまま返す
 *
 * 必要な設定（コードには書かない。wrangler secret put で預ける）
 *   【メール／必須】
 *   RESEND_API_KEY             … メールを送るサービスの鍵
 *   MAIL_TO                    … 受け取るメールアドレス（あおこさん）
 *   MAIL_FROM                  … 差出人。例 "あおこサイト <onboarding@resend.dev>"
 *
 *   【LINE／入れたい場合だけ。未設定なら黙って飛ばす】
 *   LINE_CHANNEL_ACCESS_TOKEN  … LINE公式アカウントを操作するための合言葉
 *   LINE_USER_ID               … 送り先（あおこさん自身）のID
 */

const LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push";
const RESEND_URL = "https://api.resend.com/emails";

// 入力の上限。長すぎるものは切って送る
const LIMIT = { name: 100, email: 200, body: 5000 };

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
  if (String(form.get("company") ?? "").trim() !== "") {
    // 送ったつもりで終わらせる（相手に対策を気づかせない）
    return seeOther("/thanks");
  }

  const name = cut(form.get("name"), LIMIT.name);
  const email = cut(form.get("email"), LIMIT.email);
  const body = cut(form.get("body"), LIMIT.body);

  if (!name || !email || !body || !looksLikeEmail(email)) {
    return seeOther("/sorry");
  }

  const text =
    "サイトのフォームからお問い合わせが届きました。\n" +
    "このメールにそのまま返信すると、相手に届きます。\n\n" +
    "----------------\n" +
    `お名前： ${name}\n` +
    `メール： ${email}\n` +
    "----------------\n\n" +
    body +
    "\n";

  // メールが本体。LINEは設定されていれば、ついでに送る
  const [mailOk, lineOk] = await Promise.all([
    sendMail(env, { name, email, text }),
    pushToLine(env, text),
  ]);

  // どちらか一つでも届いていれば、送信できたものとして扱う
  return seeOther(mailOk || lineOk ? "/thanks" : "/sorry");
}

async function sendMail(env, { name, email, text }) {
  if (!env.RESEND_API_KEY || !env.MAIL_TO || !env.MAIL_FROM) {
    console.error("メールの設定がありません（RESEND_API_KEY / MAIL_TO / MAIL_FROM）");
    return false;
  }

  try {
    const res = await fetch(RESEND_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
      },
      body: JSON.stringify({
        from: env.MAIL_FROM,
        to: [env.MAIL_TO],
        // 返信ボタンを押すと、相談してくれた人に返る
        reply_to: [email],
        subject: `【サイトから相談】${name} 様`,
        text,
      }),
    });

    if (!res.ok) {
      console.error("メールを送れませんでした", res.status, await res.text());
      return false;
    }
    return true;
  } catch (err) {
    console.error("メール送信サービスに接続できませんでした", err);
    return false;
  }
}

async function pushToLine(env, text) {
  // LINEを使わない場合は、設定がないので何もしない
  if (!env.LINE_CHANNEL_ACCESS_TOKEN || !env.LINE_USER_ID) return false;

  try {
    const res = await fetch(LINE_PUSH_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${env.LINE_CHANNEL_ACCESS_TOKEN}`,
      },
      body: JSON.stringify({
        to: env.LINE_USER_ID,
        // LINEは1通5000文字まで。長い相談は切って送る
        messages: [{ type: "text", text: cut(text, 4900) }],
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

function looksLikeEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}
