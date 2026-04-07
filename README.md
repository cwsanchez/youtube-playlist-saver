# YouTube Playlist Saver

A modern web app to save, track, and preserve YouTube playlist metadata. Built with **Next.js 15**, **Supabase**, and **Tailwind CSS**.

Paste a YouTube playlist URL, and the app fetches all video metadata (title, description, thumbnails, view/like counts, duration) and stores it in Supabase. Even if videos are later removed from the playlist, their data is preserved with a soft-delete timestamp.

## Features

- **Auto-detect** playlist or video URLs/IDs
- **Full metadata** preservation (title, description, thumbnail, stats, duration)
- **Soft-delete tracking** — removed videos are marked, not lost
- **Refresh** playlists to detect newly added or removed videos
- **Search & filter** saved playlists
- **Dark mode** by default with a modern, responsive UI
- **Pagination** for large playlists

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 15 (App Router, RSC, TypeScript) |
| UI | Tailwind CSS v4 + shadcn/ui |
| Database | Supabase (Postgres) |
| API | YouTube Data API v3 (server-side only) |
| Deployment | Vercel |

## Getting Started

### Prerequisites

- Node.js 18+
- A [Supabase](https://supabase.com) project
- A [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com) key

### 1. Clone & Install

```bash
git clone https://github.com/cwsanchez/youtube-playlist-saver.git
cd youtube-playlist-saver
npm install
```

### 2. Set Up Supabase

Run the SQL migration in your Supabase SQL Editor (Dashboard → SQL Editor):

```sql
-- Copy the contents of supabase/migrations/001_initial_schema.sql
```

Or use the Supabase CLI:

```bash
supabase db push
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env.local` and fill in your keys:

```bash
cp .env.example .env.local
```

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Your Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon/public key |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key (server-only) |
| `YOUTUBE_API_KEY` | YouTube Data API v3 key |

### 4. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Deploy to Vercel

1. Push to GitHub
2. Import in [Vercel](https://vercel.com/new)
3. Add the four environment variables above
4. Deploy

## Database Schema

```
channels       playlists           videos              playlists_videos
──────────     ─────────────       ──────────          ────────────────
id (PK)        id (PK)             id (PK)             playlist_id (FK)
name           name                name                video_id (FK)
created_at     description         description         removed_at
               channel_id (FK)     channel_id (FK)
               last_fetched        thumbnail_url
               created_at          published_at
                                   view_count
                                   like_count
                                   duration
                                   created_at
```

## Legacy Code

The original Python/Streamlit/Flask application is preserved in the `/legacy/` folder for reference.

## License

MIT
