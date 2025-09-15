import { getToken } from "./auth.js";
const base = "https://YOUR-N8N.onrender.com";
export async function callAgent(message, conversationId) {
  const token = await getToken();
  const r = await fetch(`${base}/webhook/agent-process`, {
    method: "POST",
    headers: { "Content-Type":"application/json", "Authorization":`Bearer ${token}` },
    body: JSON.stringify({ message, conversationId, ts: new Date().toISOString() })
  });
  if(!r.ok) throw new Error("API error"); return r.json();
}
