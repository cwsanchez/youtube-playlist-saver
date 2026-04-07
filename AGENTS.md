# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

YouTube Playlist Saver — a Next.js 15 (App Router, TypeScript) app that saves YouTube playlist/channel metadata to Supabase (Postgres). Dark-mode-first UI with shadcn/ui + Tailwind CSS v4.

### Services

| Service | Command | Port | Notes |
|---------|---------|------|-------|
| Next.js Dev | `npm run dev` | 3000 | Main app |

### Prerequisites

- **Node.js 18+**
- **Environment variables**: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `YOUTUBE_API_KEY` — set in `.env.local`.
- **Supabase tables**: Run `supabase/migrations/001_initial_schema.sql` in the Supabase SQL Editor before first use.

### Gotchas

- YouTube API calls are server-side only (Server Actions in `src/app/actions/youtube.ts`).
- The `SUPABASE_SERVICE_ROLE_KEY` is never exposed to the client.
- Legacy Python/Streamlit/Flask code lives in `/legacy/` for reference.

### Lint / Test / Build

- **Lint**: `npm run lint` (ESLint + Next.js rules)
- **Build**: `npm run build`
- **No automated test suite** currently. Test manually via the dev server.

### Project Structure

```
src/
  app/
    page.tsx              # Homepage / Dashboard
    [playlistId]/page.tsx # Playlist detail
    actions/youtube.ts    # Server Actions
    layout.tsx            # Root layout (dark mode, Toaster)
  components/             # UI components
  lib/
    supabase/             # Supabase client (server + browser)
    youtube/              # YouTube API, URL parsing, types
    format.ts             # Formatting utilities
    utils.ts              # shadcn utils
supabase/
  migrations/             # SQL migration files
legacy/                   # Old Python/Streamlit/Flask code
```
