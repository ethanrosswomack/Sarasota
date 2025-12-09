const API_URL = "https://sphinx.aetherintelligence.net/ask";
// For now, while the custom domain isn't wired, you can use:
// const API_URL = "https://sphinx-aether-api.omniversalmail.workers.dev/ask";

async function askSphinx(question) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) {
    throw new Error("API error: " + res.status);
  }

  const data = await res.json();
  return data; // { answer, chunks: [...] }
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector("#sphinx-chat-input");
  const button = document.querySelector("#sphinx-chat-send");
  const output = document.querySelector("#sphinx-chat-output");

  if (!input || !button || !output) return;

  button.addEventListener("click", async () => {
    const q = input.value.trim();
    if (!q) return;

    output.textContent = "Consulting the Halls of Amenti...";
    try {
      const data = await askSphinx(q);
      output.textContent = data.answer;
      // If you want to see sources, you could append them here.
      // console.log(data.chunks);
    } catch (err) {
      console.error(err);
      output.textContent = "Error contacting Sphinx Aether API.";
    }
  });

  // Optional: Enter key submits
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      button.click();
    }
  });
});
