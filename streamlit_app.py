# Import necessary modules for the Streamlit app
import streamlit as st
from decouple import config
from playlistRequests import request_playlist, request_channel, request_playlist_videos, request_videos, request_channel_playlists
from sqlFunctions import addPlaylist, addChannel, addVideos, addNewVideosToPlaylist, get_all_channels, get_all_playlists_for_channel, getPlaylist
from utils import extract_playlist_id, extract_channel_id
from databaseSchema import session  # For direct DB access

# Dual loading for compatibility: prefers st.secrets (for Streamlit Cloud/local with secrets.toml), falls back to decouple (for local .env)
try:
    api_key = st.secrets["SECRET_KEY"]
except (KeyError, FileNotFoundError):
    api_key = config("SECRET_KEY")

st.title("YouTube Playlist Saver")

# Sidebar for navigation - allows switching between adding data and browsing
page = st.sidebar.selectbox("Choose Action", ["Add Playlist/Channel", "Browse Saved Data"])

if page == "Add Playlist/Channel":
    st.header("Add New Data")
    # UI components for input type and URL/ID
    input_type = st.radio("Add Type", ["Playlist", "Channel"])
    url_input = st.text_input("Enter YouTube URL or ID")

    if st.button("Save to Database"):
        if not url_input:
            st.error("Please enter a URL or ID.")
        else:
            try:
                if input_type == "Playlist":
                    playlist_id = extract_playlist_id(url_input)
                    playlist_data = request_playlist(playlist_id, api_key)
                    addPlaylist(playlist_data)
                    channel_id = playlist_data["items"][0]["snippet"]["channelId"]
                    channel_data = request_channel(channel_id, api_key)
                    addChannel(channel_data)
                    video_ids = request_playlist_videos(playlist_id, api_key)
                    video_data = request_videos(video_ids, api_key)
                    addVideos(video_data)
                    addNewVideosToPlaylist(video_data, playlist_id)
                    st.success(f"Playlist '{playlist_id}' saved!")
                else:  # Channel
                    channel_id = extract_channel_id(url_input, api_key)
                    channel_data = request_channel(channel_id, api_key)
                    addChannel(channel_data)
                    playlist_ids = request_channel_playlists(channel_id, api_key)
                    for pl_id in playlist_ids:
                        pl_data = request_playlist(pl_id, api_key)
                        addPlaylist(pl_data)
                        video_ids = request_playlist_videos(pl_id, api_key)
                        video_data = request_videos(video_ids, api_key)
                        addVideos(video_data)
                        addNewVideosToPlaylist(video_data, pl_id)
                    st.success(f"Channel '{channel_id}' and playlists saved!")
            except Exception as e:
                # Error handling for API issues or invalid inputs
                st.error(f"Error: {str(e)} (Check API key/quotas or ID validity)")

elif page == "Browse Saved Data":
    st.header("Browse Saved Playlists")
    channels = get_all_channels()
    if not channels:
        st.info("No channels saved yet. Add some first!")
    else:
        # UI components for selecting channel and playlist
        channel_names = [ch.name for ch in channels]
        selected_channel = st.selectbox("Select Channel", channel_names)
        channel_id = channels[channel_names.index(selected_channel)].id

        playlists = get_all_playlists_for_channel(channel_id)
        if not playlists:
            st.info("No playlists for this channel.")
        else:
            playlist_names = [pl.name for pl in playlists]
            selected_playlist = st.selectbox("Select Playlist", playlist_names)
            playlist_id = playlists[playlist_names.index(selected_playlist)].id

            playlist = getPlaylist(playlist_id)
            if playlist:
                st.subheader(f"Playlist: {playlist.name}")
                st.write(f"Description: {playlist.description}")
                # Display videos in a table - UI component for data display
                video_data = [{"ID": v.id, "Title": v.name, "Description": v.description, "Channel ID": v.channelId} for v in playlist.videos]
                st.dataframe(video_data)
            else:
                st.error("Playlist not found.")