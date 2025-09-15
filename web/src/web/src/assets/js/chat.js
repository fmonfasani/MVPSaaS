import { callAgent } from "./api.js";

document.querySelector("#gen-btn").addEventListener("click", async () => {
  const msg = document.querySelector("#prompt").value.trim();
  const out = document.querySelector("#output");
  out.textContent = "Generando...";
  try {
    const resp = await callAgent(msg, crypto.randomUUID());
    const data = JSON.parse(resp.result);      // <- el Space devuelve JSON como string
    out.textContent = "";                      // limpia
    // render muy simple:
    out.insertAdjacentHTML("beforeend", `
      <h1 class="text-2xl font-bold">${data.title}</h1>
      <p class="mt-2 text-gray-600">${data.subtitle}</p>
      ${data.sections?.map(s => `
        <section class="mt-6">
          <h2 class="font-semibold">${s.title}</h2>
          <p class="text-sm text-gray-700">${s.body}</p>
        </section>`).join("")}
      <a class="mt-8 inline-block px-4 py-2 bg-black text-white rounded"
         href="${data.cta?.url||"/"}">${data.cta?.text||"Contactar"}</a>
    `);
  } catch (e) {
    out.textContent = "Error generando landing. Probá de nuevo.";
    console.error(e);
  }
});
