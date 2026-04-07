-- Enable RLS on all tables
ALTER TABLE channels ENABLE ROW LEVEL SECURITY;
ALTER TABLE playlists ENABLE ROW LEVEL SECURITY;
ALTER TABLE videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE playlists_videos ENABLE ROW LEVEL SECURITY;

-- Allow public read access (anon key can read)
CREATE POLICY "Allow public read" ON channels FOR SELECT USING (true);
CREATE POLICY "Allow public read" ON playlists FOR SELECT USING (true);
CREATE POLICY "Allow public read" ON videos FOR SELECT USING (true);
CREATE POLICY "Allow public read" ON playlists_videos FOR SELECT USING (true);

-- Allow service role full access (for server-side mutations via service role key)
CREATE POLICY "Allow service role all" ON channels FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow service role all" ON playlists FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow service role all" ON videos FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow service role all" ON playlists_videos FOR ALL USING (true) WITH CHECK (true);
