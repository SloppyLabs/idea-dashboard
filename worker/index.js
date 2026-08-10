/**
 * Idea Lab — community flags API.
 *
 * Public, when2meet-style: anyone picks a display name and flags the ideas they
 * think will work. No accounts, no auth — the name IS the identity.
 *
 * Storage: one KV key per (idea, person) so flag/unflag are independent writes.
 * A single shared "flags" blob would lose concurrent toggles to read-modify-write
 * races; per-key writes have no such race.
 *
 *   key   f:<ideaId>:<normalizedName>
 *   meta  { n: "<display name>" }
 *
 * Routes:
 *   GET  /api/flags  -> { "<ideaId>": ["Alice", "Bob"], ... }
 *   POST /api/flags  <- { id, name, on }  -> { ok: true }
 */

const ID_RE = /^[a-f0-9]{12}$/;
const MAX_NAME = 32;
const MAX_FLAGS = 20000; // abuse backstop for a wide-open endpoint

// Per-isolate cache so a room full of pollers doesn't hammer KV list().
let cached = { at: 0, data: null };

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...CORS },
  });

/** Identity key: case- and whitespace-insensitive, like when2meet. */
function normName(name) {
  return String(name || '').trim().replace(/\s+/g, ' ').toLowerCase();
}

function cleanName(name) {
  return String(name || '')
    .trim()
    .replace(/\s+/g, ' ')
    .replace(/[\u0000-\u001f\u007f]/g, '')
    .slice(0, MAX_NAME);
}

async function readAll(env) {
  const now = Date.now();
  if (cached.data && now - cached.at < 5000) return cached.data;

  const out = {};
  let cursor;
  do {
    const res = await env.FLAGS.list({ prefix: 'f:', limit: 1000, cursor });
    for (const k of res.keys) {
      const id = k.name.split(':')[1];
      const display = k.metadata && k.metadata.n;
      if (!id || !display) continue;
      (out[id] = out[id] || []).push(display);
    }
    cursor = res.list_complete ? null : res.cursor;
  } while (cursor);

  for (const names of Object.values(out)) names.sort((a, b) => a.localeCompare(b));
  cached = { at: now, data: out };
  return out;
}

function countFlags(map) {
  let n = 0;
  for (const names of Object.values(map)) n += names.length;
  return n;
}

async function handleSet(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'invalid JSON' }, 400);
  }

  const id = String(body.id || '');
  const display = cleanName(body.name);
  const on = body.on !== false;

  if (!ID_RE.test(id)) return json({ error: 'bad idea id' }, 400);
  if (!display) return json({ error: 'name required' }, 400);

  const key = `f:${id}:${normName(display)}`;

  if (on) {
    if (countFlags(await readAll(env)) >= MAX_FLAGS) {
      return json({ error: 'flag limit reached' }, 429);
    }
    await env.FLAGS.put(key, '1', { metadata: { n: display } });
  } else {
    await env.FLAGS.delete(key);
  }

  cached = { at: 0, data: null };
  return json({ ok: true, id, on });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });

    if (url.pathname === '/api/flags') {
      if (request.method === 'GET') return json(await readAll(env));
      if (request.method === 'POST') return handleSet(request, env);
      return json({ error: 'method not allowed' }, 405);
    }

    // Everything else is served by the static assets binding.
    return env.ASSETS.fetch(request);
  },
};
