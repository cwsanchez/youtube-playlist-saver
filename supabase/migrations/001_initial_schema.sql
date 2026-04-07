-- Initial schema for YouTube Playlist Saver
-- Migrated from SQLAlchemy models in legacy/databaseSchema.py

-- channels
CREATE TABLE IF NOT EXISTS channels (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- playlists
CREATE TABLE IF NOT EXISTS playlists (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  channel_id TEXT REFERENCES channels(id),
  last_fetched TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- videos
CREATE TABLE IF NOT EXISTS videos (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  channel_id TEXT REFERENCES channels(id),
  thumbnail_url TEXT,
  published_at TIMESTAMPTZ,
  view_count BIGINT,
  like_count BIGINT,
  duration TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- playlists_videos junction table with soft delete
CREATE TABLE IF NOT EXISTS playlists_videos (
  playlist_id TEXT REFERENCES playlists(id),
  video_id TEXT REFERENCES videos(id),
  removed_at TIMESTAMPTZ,
  PRIMARY KEY (playlist_id, video_id)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_playlists_channel_id ON playlists(channel_id);
CREATE INDEX IF NOT EXISTS idx_videos_channel_id ON videos(channel_id);
CREATE INDEX IF NOT EXISTS idx_playlists_videos_playlist_id ON playlists_videos(playlist_id);
CREATE INDEX IF NOT EXISTS idx_playlists_videos_video_id ON playlists_videos(video_id);
CREATE INDEX IF NOT EXISTS idx_playlists_videos_removed_at ON playlists_videos(removed_at);
