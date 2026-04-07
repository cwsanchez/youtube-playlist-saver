# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

YouTube Playlist Saver — a Python app that saves YouTube playlist/channel metadata to SQLite (default) or PostgreSQL. Two interfaces: **Streamlit** (primary UI) and **Flask REST API** (legacy).

### Services

| Service | Command | Port | Notes |
|---------|---------|------|-------|
| Streamlit (primary) | `streamlit run streamlit_app.py --server.port 8501 --server.headless true` | 8501 | Main UI |
| Flask API (legacy) | `python3 main.py` | 5000 | Has a pre-existing `DetachedInstanceError` on the GET `/playlist/<id>` endpoint |

### Prerequisites

- **`YOUTUBE_API_KEY`** env var must be set (injected as a Cursor secret). On startup, create `.env` with `SECRET_KEY=$YOUTUBE_API_KEY` and `.streamlit/secrets.toml` with `SECRET_KEY = "<key>"` — both are gitignored / not committed.
- The app reads the API key via `python-decouple` (`.env`) and `st.secrets` (`.streamlit/secrets.toml`). Both must exist for the full app to work.
- SQLite DB (`playlist_data.db`) is auto-created on first run.

### Gotchas

- There is no `python` binary on the VM; always use `python3`.
- `pip install` puts scripts in `~/.local/bin` — add it to `PATH` before running `streamlit`.
- The Flask API (via `databaseSchema.py`) imports Streamlit and reads `st.secrets`, so `.streamlit/secrets.toml` must exist even when running only the Flask API.
- Tests in `tests/` are interactive manual scripts (not automated test suites); they require TTY input and a valid API key.
- The `work_in_progressDockerFile` is incomplete and not functional.

### Lint / Test / Build

- **No linter configured** in the repo. You can run `python3 -m py_compile <file>` to syntax-check individual files.
- **No automated test suite**. Tests are manual scripts under `tests/`.
- **No build step** — run directly with Python.
