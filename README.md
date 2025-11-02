# YouTube Playlist Saver

This app saves YouTube playlist and channel metadata to a local SQLite database, allowing you to track videos and detect deletions over time. Originally built with a Flask backend, it now features a Streamlit frontend for easy interaction, directly using the API request and database functions.

## Features
- Add playlists or entire channels by URL or ID.
- Browse saved channels, playlists, and videos via dropdowns.
- Supports URL parsing for playlists (e.g., ?list=...) and channels (e.g., /channel/UC... or @handle).
- Database stores metadata to preserve history even if videos are deleted on YouTube.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add your YouTube API key to `.env`: `SECRET_KEY="YOUR_KEY_HERE"`
3. Run the app: `streamlit run streamlit_app.py`

Optional: For PostgreSQL (e.g., Neon), set DATABASE_URL in .streamlit/secrets.toml (local) or Streamlit Cloud secrets (TOML format): DATABASE_URL = "postgresql://user:password@host.neon.tech/dbname?sslmode=require"
Note: Create the DB on Neon first. The app will create tables if missing.

Note: If you encounter database schema errors after updating the app, delete `playlist_data.db` and re-add your data.

## Usage
- **Add Data**: Enter a playlist/channel URL or ID, select type, and save.
- **Browse**: Select channel > playlist to view details in a table.

## Deployment to Streamlit Cloud
1. Push your repo to GitHub.
2. Create a new app on share.streamlit.io, link to your repo and streamlit_app.py.
3. In app settings > Secrets, add: SECRET_KEY = "your_youtube_api_key_here" (in TOML format, with quotes).
4. Redeploy.

Note: The original Flask API (run via `python main.py`) is retained for future extensions but not used in the Streamlit app.

## Dependencies
- Streamlit for frontend
- Requests, SQLAlchemy, etc., for backend logic (see requirements.txt)
