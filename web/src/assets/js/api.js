export async function callAgent(message, conversationId) {
  const base = "https://fmonfasani-mvpsaas.hf.space";
  const r = await fetch(`${base}/agent-process`, {
    method: "POST",
    headers: { "Content-Type":"application/json" },
    body: JSON.stringify({ message, conversationId })
  });
  if (!r.ok) throw new Error(`API error ${r.status}`);
  return r.json();
}
export async function callAgent(message, conversationId) {
  const base = "https://fmonfasani-mvpsaas.hf.space";
  const r = await fetch(`${base}/agent-process`, {
    method: "POST",
    headers: { "Content-Type":"application/json" },
    body: JSON.stringify({ message, conversationId })
  });
  if (!r.ok) throw new Error(`API ${r.status}`);
  return r.json(); // { success, result: "<json string>", error }
}
