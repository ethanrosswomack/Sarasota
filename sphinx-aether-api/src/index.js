export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
      });
    }

    // Proxy POST /ask to the backend
    if (url.pathname === "/ask" && request.method === "POST") {
      const body = await request.text();

      const backendUrl = (env && env.BACKEND_URL) ? env.BACKEND_URL : "http://127.0.0.1:8000";
      const backendRes = await fetch(backendUrl.replace(/\/+$/, "") + "/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body,
        // pass through credentials if needed
      });

      // Copy response body and status, and set CORS header
      const resHeaders = new Headers(backendRes.headers);
      resHeaders.set("Access-Control-Allow-Origin", "*");

      const bodyStream = backendRes.body;

      return new Response(bodyStream, {
        status: backendRes.status,
        headers: resHeaders,
      });
    }

    if (url.pathname === "/health") {
      const backendUrl = (env && env.BACKEND_URL) ? env.BACKEND_URL : "http://127.0.0.1:8000";
      return new Response(JSON.stringify({ status: "ok", backend: backendUrl }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }

    return new Response("Sphinx Aether API", { status: 200 });
  },
};
