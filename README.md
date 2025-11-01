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

## Usage
- **Add Data**: Enter a playlist/channel URL or ID, select type, and save.
- **Browse**: Select channel > playlist to view details in a table.

Note: The original Flask API (run via `python main.py`) is retained for future extensions but not used in the Streamlit app.

## Dependencies
- Streamlit for frontend
- Requests, SQLAlchemy, etc., for backend logic (see requirements.txt)
