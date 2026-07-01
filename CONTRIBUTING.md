# Contributing to brawlstars-twitch

Thank you for your interest in contributing! This project welcomes pull requests, bug reports, and feature suggestions. Whether you're fixing a bug, adding a feature, or improving documentation, your help makes this streaming overlay better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Style Guide](#style-guide)
- [Reporting Issues](#reporting-issues)
- [Project Structure](#project-structure)
- [Architecture Overview](#architecture-overview)

## Code of Conduct

This project is inclusive and respectful. By participating, you agree to:

- Be respectful and constructive in all interactions
- Avoid discrimination, harassment, and toxic behavior
- Welcome feedback and differing viewpoints
- Focus on the code, not the person

Violations should be reported privately to the maintainer.

## Getting Started

### Prerequisites

- **Python 3.9+** (3.10+ recommended)
- **pip** (Python package manager)
- **Git**
- A **Twitch Developer Application** (for testing with real integration; see README for setup)
- **Node.js** (optional; for any future frontend tooling)

### Fork & Clone

1. Fork this repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/brawlstars-twitch.git
   cd brawlstars-twitch
   ```
3. Add the original repo as upstream to stay in sync:
   ```bash
   git remote add upstream https://github.com/Ladididididideyo/brawlstars-twitch.git
   ```

## Development Setup

### 1. Create a Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

For development, you may also want to install linting/formatting tools:

```bash
pip install black flake8 pylint
```

### 3. Configure Environment

Copy the `.env.example` file (or see the README for the template) to `.env`:

```bash
cp example_.env.txt .env
```

Fill in your values:

```
APPLICATION_CLIENT_ID=<your-twitch-client-id>
APPLICATION_CLIENT_SECRET=<your-twitch-client-secret>
WEB_SERVER_PORT=1234
```

For local testing without Twitch, you can enable demo mode by setting `DEMO_MODE = True` in `server.py`.

### 4. Run the Server

```bash
python server.py
```

The server will start on the port specified in `.env`. You can access the overlay at:

```
http://localhost:WEB_SERVER_PORT/followers_rank
```

## Making Changes

### Branch Strategy

1. Create a new branch from `main` for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes
   git checkout -b fix/your-bug-fix
   ```

2. Make your changes in focused commits with clear messages:
   ```bash
   git commit -m "Add feature X" -m "Detailed description of what changed and why"
   ```

### Code Style

- **Python**: Follow [PEP 8](https://pep8.org/) conventions
  - Use 4-space indentation
  - Keep lines under 100 characters
  - Use descriptive variable and function names
  - Add docstrings to functions and classes

- **JavaScript**: Use consistent formatting
  - 2-space indentation
  - Use `const` and `let` instead of `var`
  - Add comments for complex logic

- **HTML/CSS**: Keep templates clean and readable
  - Use semantic HTML where possible
  - Keep CSS scoped to avoid global pollution

### Testing Your Changes

1. **Manual Testing**:
   - Test the overlay locally using the demo mode or your own Twitch account
   - Verify animations and audio playback work smoothly
   - Test in OBS as a Browser Source if your changes affect the frontend

2. **Code Review Checklist**:
   - Code is readable and follows the style guide
   - No hardcoded values; use config or environment variables
   - No debug statements left behind (`print()`, `console.log()`)
   - Credentials are never logged or exposed

### Performance Considerations

This project runs on streaming machines, so performance matters:

- Avoid blocking operations on the main event loop (see `playsound` blocking issue)
- Use async/await patterns where possible
- Keep assets (images, audio) reasonably sized
- Test with multiple rapid events (simulate high follower activity)

## Submitting a Pull Request

### Before You Submit

1. **Sync with upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test thoroughly**:
   - Run locally with demo mode enabled
   - Test with real Twitch integration if your changes affect it
   - Verify no regressions in existing functionality

3. **Check your commits**:
   - Squash related commits into logical units
   - Write clear, descriptive commit messages
   - Reference any related issues (e.g., "Fixes #42")

### PR Guidelines

- **Title**: Use a clear, concise title (e.g., "Add async audio playback" or "Fix SSE event stream blocking")
- **Description**: Include:
  - What problem does this solve or what feature does it add?
  - How did you test it?
  - Any breaking changes or migration steps?
  - Relevant links to issues or discussions
- **Keep it focused**: One feature or fix per PR makes review easier
- **Update docs**: If your change affects setup, configuration, or usage, update the README or add inline comments

### Example PR Description

```markdown
## Summary
Fixes the blocking audio playback issue that was causing SSE event delays.

## Changes
- Moved `playsound()` call to a background thread to prevent blocking the event stream
- Added a thread-safe queue for audio playback requests
- Updated audio handling to process sounds asynchronously

## Testing
- Tested with rapid follower events (5 followers in 2 seconds)
- Verified audio still plays correctly on each follower event
- No event stream delays observed

## Notes
This is a performance-critical change for streamers with high follower velocity.
```

## Style Guide

### Python

```python
# Good
def process_follower_event(username: str, rank: str) -> None:
    """
    Process a new follower event and add to queue.
    
    Args:
        username: The follower's username
        rank: The assigned rank (Bronze, Silver, etc.)
    """
    follower_data = {"username": username, "rank": rank}
    new_follower_queue.put(follower_data)
    logger.info(f"{username} followed with rank {rank}")

# Avoid
def process_follow(u, r):
    # Add to queue
    new_follower_queue.put({"username": u, "rank": r})
    print(u + " followed")
```

### JavaScript

```javascript
// Good
function createRankedIconBitmap(rank, x = 500, y = 0, opacity = 0) {
    const imageUrl = `${staticFileEndpoint}ranked_images/${rank}.png`;
    const bitmap = new createjs.Bitmap(imageUrl);
    bitmap.alpha = opacity;
    bitmap.x = x;
    bitmap.y = y;
    return bitmap;
}

// Avoid
function createRankedIconBitmap(r, x, y, o) {
    var b = new createjs.Bitmap(staticFileEndpoint + "ranked_images/" + r + ".png");
    b.alpha = o;
    b.x = x;
    b.y = y;
    return b;
}
```

## Reporting Issues

### Bug Reports

Include:
- **Title**: A clear, descriptive title
- **Environment**: Python version, OS, browser (if frontend issue)
- **Steps to reproduce**: Exact steps to trigger the issue
- **Expected vs. actual behavior**: What should happen vs. what does happen
- **Error message or log**: Full stack trace if available
- **Screenshots/video**: If it's a visual issue

### Feature Requests

Include:
- **Use case**: Why would this feature be useful?
- **Proposed solution**: How should it work?
- **Alternatives**: Any other ways to achieve this?
- **Additional context**: Any relevant discussion or inspiration

## Project Structure

```
brawlstars-twitch/
├── server.py                      # Main Flask app + Twitch EventSub integration
├── requirements.txt               # Python dependencies
├── example_.env.txt               # Environment template
├── README.md                       # Project documentation
├── CONTRIBUTING.md                # This file
├── LICENSE                        # GNU GPL v3
├── static/
│   ├── ranked_images/             # Per-rank rank icons (PNG)
│   ├── ranked_audio/              # Per-rank audio cues (MP3)
│   ├── ranked_text/               # Per-rank overlay text (TXT)
│   └── fonts/                     # Custom fonts (TTF)
├── templates/
│   └── follower_rank.html         # Frontend overlay (Canvas + CreateJS)
├── install_venv.bat               # Windows virtualenv setup
└── start_server.bat               # Windows server launcher
```

## Architecture Overview

### Backend (Python + Flask)

- **Twitch Integration**: EventSub WebSocket listens for channel follow events
- **Queue-based Event Flow**: Followers enter a Queue and are consumed by the SSE endpoint
- **Demo Mode**: Generates fake follow events for testing without Twitch
- **Audio Playback**: Per-rank audio triggered on the backend (keeps audio on stream machine)

### Frontend (HTML5 + Canvas + CreateJS)

- **EventSource (SSE)**: Subscribes to `/follower_stream` for real-time events
- **Canvas Rendering**: CreateJS Ticker drives 120 FPS animations
- **Animations**: Rank icons bounce in with easing; text fades with outlines
- **Text Templates**: Dynamic substitution of `[USERNAME]` placeholder per-rank

### Data Flow

```
Twitch EventSub
    |
    v
on_follow() callback
    |
    v
new_follower_queue.put(follower_info)
    |
    v
/follower_stream (SSE endpoint)
    |
    v
Frontend EventSource listener
    |
    v
Create animations + fetch rank text template
    |
    v
Play rank audio + render overlay
```

## Known Issues & Opportunities for Contribution

See the README "Contribute" section for suggested improvements:

- [ ] Add environment variable toggle for demo mode
- [ ] Replace in-memory queue with Redis for multi-process reliability
- [ ] Add support for additional event types (subs, cheers, raids)
- [ ] Async audio playback to prevent event stream blocking
- [ ] Persistent Twitch token storage (instead of ephemeral auth)
- [ ] Unit and integration tests
- [ ] CI/CD workflow (GitHub Actions)

## Questions?

- Open a GitHub Issue for bugs, features, or questions
- Check existing issues and discussions first to avoid duplicates
- Be descriptive and provide context

Thank you for contributing!
