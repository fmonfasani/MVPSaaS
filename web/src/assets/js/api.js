const base = "https://fmonfasani-mvpsaas.hf.space"; // Space
export async function callAgent(message, conversationId) {
  const r = await fetch(`${base}/agent-process`, {
    method: "POST",
    headers: { "Content-Type":"application/json" },
    body: JSON.stringify({ message, conversationId })
  });
  if(!r.ok) throw new Error("API error");
  return r.json();
}
