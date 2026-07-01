# brawlstars-twitch

Turn your Twitch followers into an exciting, animated Brawl Stars-style overlay — complete with rank art, custom text, and per-rank audio cues. Perfect for livestreamers who want immediate, high-impact follower alerts that match the Brawl Stars aesthetic.

Why this project?
- Plug-and-play overlay: a browser-based overlay you can add to OBS as a Browser Source.
- Twitch EventSub integration: listens for channel follows in real-time and streams events to the overlay.
- Customizable assets: swap images, audio, and text per-rank to match your brand.
- Lightweight and local: runs on your streaming machine, no paid services required.

Live demo (local):
1. Configure `.env` (copy from `example_.env.txt`) with your Twitch app credentials and desired `WEB_SERVER_PORT`.
2. Start the app: `python server.py` (or use `start_server.bat` on Windows).
3. In OBS, add a Browser Source pointing to `http://localhost:<WEB_SERVER_PORT>/followers_rank` (set width/height to 1000x1000 for default layout).

Features
- Animated rank icon with smooth easing and outline text
- Per-rank audio clips (played locally on the backend for stream machine audio)
- Demo mode for testing without Twitch followers
- Easy to customize: add images to `static/ranked_images/`, audio to `static/ranked_audio/`, text templates to `static/ranked_text/`, and fonts to `static/fonts/`.

Quick install

Requirements:
- Python 3.9+ (recommended)
- pip

Steps:
1. Clone the repo
   git clone https://github.com/Ladididididideyo/brawlstars-twitch
2. Create a virtualenv and install requirements:
   python -m venv .venv
   .venv\Scripts\activate       # Windows
   source .venv/bin/activate    # macOS / Linux
   pip install -r requirements.txt
3. Copy `example_.env.txt` to `.env` and populate:
   - APPLICATION_CLIENT_ID
   - APPLICATION_CLIENT_SECRET
   - WEB_SERVER_PORT (e.g. 1234)
4. Run the server:
   python server.py

Configuration notes
- The app reads config from `.env` via python-dotenv. Use `example_.env.txt` as a template.
- To quickly test the overlay without Twitch integration enable `DEMO_MODE = True` in `server.py` or ask me and I can add an env var toggle.

OBS / Browser Source settings
- URL: `http://<machine-ip>:<WEB_SERVER_PORT>/followers_rank`
- Width / Height: 1000 x 1000 (matches the default canvas size)
- FPS: 60
- If you host the app on your streaming machine and OBS is on the same machine, use `localhost`.

Customize
- Images: replace files in `static/ranked_images/` with PNGs named exactly as the rank keys (e.g. `Bronze.png`, `Legendary.png`).
- Audio: place MP3 files in `static/ranked_audio/` named exactly like the rank keys.
- Text: edit `static/ranked_text/<Rank>.txt` to change the overlay text. Use `[USERNAME]` as placeholder.
- Font: add TTF file to `static/fonts/` and update the `@font-face` rule in `templates/follower_rank.html`.

Security & production
- Keep your Twitch credentials secret. Do not commit `.env` to your repo.
- For public streaming setups use HTTPS and deploy behind a reverse proxy. Persist auth storage for tokens instead of ephemeral memory.

Contribute
- Pull requests welcome. Ideas:
  - Add env-driven demo toggle
  - Replace in-memory queue with Redis for multi-process reliability
  - Add more event types (subs, cheers, raids) and overlay pages for each

License
- This project is licensed under the GNU GPL v3; see LICENSE for details.

Credits
- Built by Ogr1sh (2026). Uses twitchAPI, Flask, CreateJS, and playsound3.

