# Import necessary modules for the Streamlit app
import streamlit as st
from decouple import config
from playlistRequests import request_playlist, request_channel, request_playlist_videos, request_videos, request_channel_playlists
from sqlFunctions import addPlaylist, addChannel, addVideos, addNewVideosToPlaylist, get_all_channels, get_all_playlists_for_channel, getPlaylist, refresh_playlist, get_active_videos, get_removed_videos, queryPlaylistVideo
from utils import extract_playlist_id, extract_channel_id
from databaseSchema import session  # For direct DB access

# Dual loading for compatibility: prefers st.secrets (for Streamlit Cloud/local with secrets.toml), falls back to decouple (for local .env)
try:
    api_key = st.secrets["SECRET_KEY"]
except (KeyError, FileNotFoundError):
    api_key = config("SECRET_KEY")

st.title("YouTube Playlist Saver")

# Sidebar for navigation - allows switching between adding data and browsing
if st.sidebar.button("Add Playlist/Channel"):
    st.session_state.page = "add"
if st.sidebar.button("Browse Saved Data"):
    st.session_state.page = "browse"

if st.session_state.get("page") == "add" or not st.session_state.get("page"):
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
                    progress = st.progress(0)
                    for i, pl_id in enumerate(playlist_ids):
                        pl_data = request_playlist(pl_id, api_key)
                        addPlaylist(pl_data)
                        video_ids = request_playlist_videos(pl_id, api_key)
                        video_data = request_videos(video_ids, api_key)
                        addVideos(video_data)
                        addNewVideosToPlaylist(video_data, pl_id)
                        progress.progress((i + 1) / len(playlist_ids))
                    st.success(f"Channel '{channel_id}' and playlists saved!")
            except Exception as e:
                # Error handling for API issues or invalid inputs
                if "quota" in str(e).lower():
                    st.error("API quota likely exceeded. Wait 24h or get more quota.")
                else:
                    st.error(f"Error: {str(e)} (Check API key or ID validity)")

if st.session_state.get("page") == "browse":
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
                st.write(f"Last refreshed: {playlist.last_fetched if playlist.last_fetched else 'Never'}")
                if st.button("Refresh Playlist"):
                    with st.spinner("Refreshing..."):
                        refresh_playlist(playlist_id, api_key)
                    st.rerun()

                active_videos = get_active_videos(playlist_id)
                video_data = [{"No.": i+1, "ID": v.id, "Title": v.name, "Description": v.description, "Channel ID": v.channelId, "Views": v.view_count, "Likes": v.like_count, "Duration": v.duration, "Published": v.published_at.strftime("%Y-%m-%d %H:%M") if v.published_at else ""} for i, v in enumerate(active_videos)]
                st.dataframe(video_data, height=400)

                removed_videos = get_removed_videos(playlist_id)
                count = len(removed_videos)
                if count > 0:
                    st.warning(f"{count} items have been deleted from this playlist")
                    st.subheader("Deleted Videos")
                    removed_data = [{"ID": v.id, "Title": v.name, "Description": v.description, "Channel ID": v.channelId, "Views": v.view_count, "Likes": v.like_count, "Duration": v.duration, "Published": v.published_at.strftime("%Y-%m-%d %H:%M") if v.published_at else "", "Removed At": queryPlaylistVideo(v.id, playlist_id).removed_at.strftime("%Y-%m-%d %H:%M") if queryPlaylistVideo(v.id, playlist_id).removed_at else ""} for v in removed_videos]
                    st.dataframe(removed_data, height=200)
                else:
                    st.success("No videos have been deleted!")
            else:
                st.error("Playlist not found.")