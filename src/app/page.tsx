import { getPlaylists } from "@/app/actions/youtube";
import { SaveInput } from "@/components/save-input";
import { PlaylistSearch } from "@/components/playlist-search";
import { ListVideo } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  let playlists: Awaited<ReturnType<typeof getPlaylists>> = [];
  let error: string | null = null;

  try {
    playlists = await getPlaylists();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load playlists";
  }

  return (
    <main className="flex-1">
      <div className="max-w-5xl mx-auto px-4 py-12">
        {/* Hero */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10 mb-6">
            <ListVideo className="h-8 w-8 text-primary" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-3">
            YouTube Playlist Saver
          </h1>
          <p className="text-muted-foreground text-lg max-w-md mx-auto">
            Save and track YouTube playlists. Preserve video metadata even after
            deletion.
          </p>
        </div>

        {/* Save Input */}
        <div className="flex justify-center mb-12">
          <SaveInput />
        </div>

        {/* Error State */}
        {error && (
          <div className="text-center p-8 rounded-lg border border-destructive/50 bg-destructive/10 mb-8">
            <p className="text-destructive">{error}</p>
            <p className="text-sm text-muted-foreground mt-2">
              Make sure your Supabase credentials are configured correctly.
            </p>
          </div>
        )}

        {/* Playlist List */}
        {playlists.length > 0 ? (
          <PlaylistSearch playlists={playlists} />
        ) : (
          !error && (
            <div className="text-center py-16">
              <ListVideo className="h-12 w-12 text-muted-foreground/30 mx-auto mb-4" />
              <h2 className="text-xl font-medium text-muted-foreground">
                No playlists saved yet
              </h2>
              <p className="text-sm text-muted-foreground/60 mt-1">
                Paste a YouTube playlist URL above to get started.
              </p>
            </div>
          )
        )}
      </div>
    </main>
  );
}
