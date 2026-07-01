# brawlstars-twitch

Turn your Twitch followers into an exciting, animated Brawl Stars-style overlay — complete with rank art, custom text, and per-rank audio cues. Perfect for livestreamers who want immediate, high-impact follower alerts that match the Brawl Stars aesthetic.

Why this project?
- Plug-and-play overlay: a browser-based overlay you can add to OBS as a Browser Source.
- Twitch EventSub integration: listens for channel follows in real-time and streams events to the overlay.
- Customizable assets: swap images, audio, and text per-rank to match your brand.
- Lightweight and local: runs on your streaming machine, no paid services required.

Register your Twitch application
1. Before creating your `.env`, register an application at https://dev.twitch.tv/docs/authentication/register-app.
2. When registering the app, set the OAuth Redirect URL to:
   `http://localhost:<YOUR_WEB_SERVER_PORT>/follower_rank`
   (replace `<YOUR_WEB_SERVER_PORT>` with the port you plan to use, e.g. `1234`).
3. After registering, copy `example_.env.txt` to `.env` and set:
   - `APPLICATION_CLIENT_ID` to the Client ID from your app,
   - `APPLICATION_CLIENT_SECRET` to the Client Secret,
   - `WEB_SERVER_PORT` to the same port you used in the OAuth Redirect URL above.

Live demo (local)

After you register the app and create your `.env`, follow these steps to get the overlay running locally:

1. Install virtualenv and dependencies (Windows helper included):
   - Double-click `install_venv.bat` to create a virtual environment and install requirements (Windows).
   - On macOS/Linux, run the steps in the "Quick install" section below.

2. Start the server:
   - Double-click `start_server.bat` (Windows) or run `python server.py` in your activated virtualenv.

3. Authorize the application:
   - When the server starts it may print an authorization URL or prompt you to authorize the app. Open that URL in your browser and complete the OAuth flow for the Twitch app you registered (ensure you authorize with the broadcaster/moderator account you want to monitor).
   - If you set the OAuth Redirect URL to `http://localhost:<WEB_SERVER_PORT>/follower_rank`, the OAuth flow will redirect to that page after authorization.

4. Add the overlay to OBS:
   - In OBS click the + button in Sources and choose "Browser".
   - In the Browser source properties set the URL to:
     `http://localhost:<WEB_SERVER_PORT>/followers_rank`
     (replace `<WEB_SERVER_PORT>` with the port you set in `.env`).
   - Set Width and Height to `1000` and `1000` (matches the default canvas).
   - Click OK. You're done — resize the source in OBS however you like.

Features
- Animated rank icon with smooth easing and outline text
- Per-rank audio clips (played locally on the backend for stream machine audio)
- Demo mode for testing without Twitch followers
- Easy to customize: add images to `static/ranked_images/`, audio to `static/ranked_audio/`, text templates to `static/ranked_text/`, and fonts to `static/fonts/`.

Quick install

Requirements:
- Python 3.9+ (recommended)
- pip

Steps (manual)
1. Clone the repo
   ```bash
   git clone https://github.com/Ladididididideyo/brawlstars-twitch
   ```
2. Create a virtualenv and install requirements:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Copy `example_.env.txt` to `.env` and populate the values as described above.
4. Run the server:
   ```bash
   python server.py
   ```

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
