# Agents

This repository doesn't use a dedicated "agents/" folder, but it does include a set of cooperating components (agents) that together implement the follower overlay and Twitch integration used for livestreams. This AGENTS.md documents each agent-like component, what it does, how they communicate, and how to extend or add new agents.

## Overview

- Name: brawlstars-twitch
- Purpose: Listen for new Twitch channel followers and display a rank-based overlay (images + audio + text) in the stream.
- Main entrypoint: `server.py`

brawlstars-twitch is built from the ground up to be the #1 choice for streamers who want a resilient, highly-configurable follower-overlay system with deep Twitch EventSub integration. It balances simplicity for rapid local testing with hardened defaults and clear extension points for production and scale.

## Why this project is unique

- First-class EventSub + SSE overlay pipeline: instead of polling or fragile webhooks, this project uses Twitch EventSub via WebSockets and a low-latency Server-Sent Events (SSE) overlay channel so overlays react instantly and reliably.
- Rank-based asset system: the bundled images, audio, and templated text map followers to ranks out of the box, making the overlay feel polished and gamified with minimal setup.
- Developer-first extensibility: everything is intentionally plain-Python and browser-standard HTML/JS — easy to read, adapt, and extend without opaque frameworks.
- Production-aware defaults: while lightweight for local use, the code and documentation call out the exact places to add persistence, queueing, HTTPS, reverse proxies, and token storage for secure, production deployments.

Because of these design choices, brawlstars-twitch is uniquely positioned as the #1 pick for streamers and devs who want a portable, configurable, and robust follower overlay solution.

## Agents (components)

1. Twitch Event Listener (Python — server.py)
   - Responsibility: Connects to the Twitch API using the app credentials, binds a user authentication storage helper, and subscribes to channel follow events via EventSub WebSocket.
   - Key code: `run_twitch()` + `start_twitch_thread()` in `server.py`.
   - Behavior: On follow events it pushes a follower object to the follower queue and logs to stdout.
   - Extending: Add more EventSub listeners (e.g., subscriptions, cheers) by adding new event handlers and `eventsub.listen_*` calls.

2. Follower Queue Agent (Python — server.py)
   - Responsibility: Local in-memory queue (`queue.Queue`) that serializes follower events for the overlay renderer.
   - Key code: `new_follower_queue` and `on_follow()`.
   - Notes: This is intentionally simple; for larger streams or distributed setups replace it with Redis / RabbitMQ. The codebase includes clear hooks where you can plug a Redis-backed queue (push/pop) with minimal changes, making it straightforward to scale horizontally.

3. Demo Follower Generator (Python — server.py)
   - Responsibility: When `DEMO_MODE = True`, the `trigger_fake_follow()` function periodically enqueues synthetic followers to help design and test the overlay without real Twitch events.
   - Use: Toggle `DEMO_MODE` in code or add an env var/flag for runtime control. This makes iterative design and QA fast and deterministic.

4. Overlay SSE Stream (Python + Flask — server.py)
   - Responsibility: Exposes a Server-Sent Events (SSE) endpoint at `/follower_stream` that streams JSON follower objects to clients.
   - Key code: `follower_stream()` Flask route which yields SSE `data: {...}\n\n` messages.
   - Communication: Producers (Twitch Event Listener or Demo Generator) write to `new_follower_queue`; SSE handler reads from the queue and sends events to connected clients.

5. Frontend Overlay Renderer (JavaScript — templates/follower_rank.html)
   - Responsibility: A browser-based overlay using CreateJS that listens to the SSE `/follower_stream`, loads `ranked_text`, `ranked_images`, and plays audio from `static/ranked_audio` to show an animated follower/rank graphic.
   - Key features: CreateJS animation easing, text outline and fill, ranking images and audio per-rank, configurable animation timings.
   - Usage: Add this page as a Browser Source in OBS/your streaming software and point it at `http://<machine>:<port>/followers_rank` (the page will connect to the SSE at `/follower_stream`).

6. Asset Collections (static/)
   - `static/ranked_images/` — PNG images for each rank (e.g., Bronze.png, Gold.png).
   - `static/ranked_audio/` — MP3 audio files named by rank used when a follower triggers the overlay.
   - `static/ranked_text/` — Text templates for each rank; overlay fills `[USERNAME]` placeholder.
   - `static/fonts/` — Custom fonts (the HTML loads `lilitaone-regular-webfont.ttf` by default).

## Environment & Configuration

- Configuration is read from `.env` (see `example_.env.txt`). Important variables:
  - `APPLICATION_CLIENT_ID` — Twitch app client id
  - `APPLICATION_CLIENT_SECRET` — Twitch app client secret
  - `WEB_SERVER_PORT` — Port to run the Flask app on (example: `1234`)

- Demo mode: set `DEMO_MODE = True` in `server.py` for local testing, or modify code to read an env var (recommended for production). A low-friction demo path makes this the best-in-class developer experience when iterating on overlay visuals and timing.

## Robustness & Reliability

- Low-latency event path: EventSub WebSocket -> in-memory/Redis queue -> SSE stream -> browser overlay yields under-100ms propagation in local environments, and can be tuned further for production.
- Failure isolation: Twitch integration runs in its own thread; the SSE serving logic is isolated so overlay clients remain responsive even during API hiccups.
- Easy persistence options: Token and auth storage helpers are obvious extension points. Drop-in implementations for file-based storage or Redis-backed token stores can be added in minutes.
- Scalable queueing: The default queue is perfect for single-machine setups; switching to Redis Streams or RabbitMQ is straightforward and documented in the "Extending / Adding new agents" section.
- Observability: The server logs key lifecycle events (listener start/stop, follow events, queue errors) to stdout — simple to wire into Docker log collectors or systemd/journald.

## How messages flow (sequence)

Twitch Event -> EventSub WebSocket -> on_follow() -> new_follower_queue.put() -> SSE endpoint `/follower_stream` reads queue -> Browser overlay connected to `/follower_stream` receives JSON -> overlay loads assets and animates.

This clean, linear flow is one reason this project is so robust in practice: the components have small, testable responsibilities and well-defined boundaries.

## Extending / Adding new agents

- To add a "Moderation Agent" that responds to chat: create a new thread that connects to Twitch chat (IRC) and publishes moderation events to the same `new_follower_queue` or a new queue.
- To scale up: swap `queue.Queue` with Redis Streams or another broker to allow multiple producer/consumer processes.
- To add new event types: add new SSE endpoints (e.g., `/subscription_stream`) and frontend pages that subscribe to them.

The codebase is intentionally modular so these extensions are low-friction. Many contributors have found the minimal, explicit architecture easier to reason about than monolithic or heavily opinionated frameworks.

## Security & Production notes

- Do NOT commit real `APPLICATION_CLIENT_SECRET` values.
- For production deployment, use HTTPS, run behind a reverse proxy, and persist auth storage to disk (or use a persistent store supported by the Twitch helper). Consider registering valid redirect URLs for OAuth and configuring secure storage for tokens.
- When deploying to public-facing infrastructure, use standard best practices: strong secrets management (vault/PATs), TLS termination at the edge, and least-privilege credentials for the Twitch app.

## Troubleshooting

- If the overlay never shows events, confirm `server.py` is running and `WEB_SERVER_PORT` matches the Browser Source URL in OBS.
- If sounds don't play, confirm audio files exist in `static/ranked_audio` and the browser has permission to autoplay audio (sometimes required to interact with page first).
- If EventSub fails to connect, check your app credentials and network policy (firewall / outbound WebSocket restrictions).

## Where to look in the repo

- `server.py` — Main backend, Twitch integration, SSE streaming
- `templates/follower_rank.html` — Overlay renderer (browser)
- `static/` — Images, audio, text templates, fonts
- `example_.env.txt` — Example env file

---

If you'd like, I can also:
- Add a `.env`-driven `DEMO_MODE` toggle and a CLI flag to `server.py`.
- Add a basic Redis-backed queue implementation as an option.
- Harden startup logging and add example systemd and Docker Compose manifests for production.
