# Deploying the Sphinx Aether Worker (front door) and Traefik config

This doc describes the steps to expose your local Voyagers API and create a Cloudflare Worker that proxies `/ask`.

## 1. Verify Voyagers API is reachable

Run your Voyagers API on omniversal-core:

```bash
uvicorn voyagers_api:app --host 0.0.0.0 --port 8000
```

Test locally (from the host):

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the Halls of Amenti?"}'
```

## 2. Add Traefik dynamic config

File: `deploy/traefik_voyagers_dynamic.yml` (already added).

- Ensure `servers.url` points to a host reachable from Traefik (e.g. `http://omniversal-core:8000` or `http://host.docker.internal:8000`).
- Reload Traefik.
- Create a DNS A record for `voyagers-api.aetherintelligence.net` pointing to your Traefik entry IP.

Test the public endpoint once DNS propagates:

```bash
curl -X POST https://voyagers-api.aetherintelligence.net/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the Halls of Amenti?"}'
```

## 3. Deploy the Cloudflare Worker

Files in `sphinx-aether-api/`:

- `src/index.js` — Worker code that proxies `/ask` to the backend
- `wrangler.toml` — worker config (BACKEND_URL is set to `https://voyagers-api.aetherintelligence.net`)

Install wrangler and deploy:

```bash
npm install -g wrangler
cd sphinx-aether-api
npx wrangler deploy
```

This returns a `workers.dev` URL. Test:

```bash
curl -X POST "https://<your-worker>.workers.dev/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the Halls of Amenti?"}'
```

If everything works, add a Custom Domain in the Cloudflare Dashboard for the worker and point `sphinx.aetherintelligence.net` at it.

## 4. Frontend

Update your chat UI to POST to `https://sphinx.aetherintelligence.net/ask`.

## Security notes

- If you expose Ollama or the API publicly, secure it with authentication (mTLS, token, IP allowlist, or Cloudflare Access).
- Use Cloudflare Access or Workers KV/Secrets to store sensitive keys if needed.

---

If you want, I can also:

- Add a small `wrangler publish` example that shows how to set `BACKEND_URL` from the CLI instead of `wrangler.toml`.
- Add a sample `cloudflared` config for local tunneling.
- Add a small test script that your front-end can call for health-checking the Worker.
