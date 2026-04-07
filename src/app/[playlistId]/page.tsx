import { getPlaylistDetail } from "@/app/actions/youtube";
import { RefreshButton } from "@/components/refresh-button";
import { VideoTable } from "@/components/video-table";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  ArrowLeft,
  ListVideo,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { formatDistanceToNow } from "date-fns";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ playlistId: string }>;
}

export default async function PlaylistDetailPage({ params }: PageProps) {
  const { playlistId } = await params;
  const data = await getPlaylistDetail(playlistId);

  if (!data) notFound();

  const { playlist, activeVideos, removedVideos } = data;
  const channelName =
    (playlist.channels as { name: string } | null)?.name ?? "Unknown Channel";

  return (
    <main className="flex-1">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Back nav */}
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors mb-6"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to playlists
        </Link>

        {/* Playlist Header */}
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-6">
          <div className="min-w-0">
            <div className="flex items-center gap-3 mb-2">
              <ListVideo className="h-7 w-7 text-primary shrink-0" />
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight truncate">
                {playlist.name}
              </h1>
            </div>
            <p className="text-muted-foreground">{channelName}</p>
            {playlist.description && (
              <p className="text-sm text-muted-foreground mt-2 max-w-2xl">
                {playlist.description}
              </p>
            )}
            <div className="flex items-center gap-3 mt-3 flex-wrap">
              <Badge variant="secondary">
                {activeVideos.length} active video
                {activeVideos.length !== 1 ? "s" : ""}
              </Badge>
              {removedVideos.length > 0 && (
                <Badge variant="destructive" className="gap-1">
                  <AlertTriangle className="h-3 w-3" />
                  {removedVideos.length} removed
                </Badge>
              )}
              {playlist.last_fetched && (
                <span className="text-xs text-muted-foreground">
                  Last refreshed{" "}
                  {formatDistanceToNow(new Date(playlist.last_fetched), {
                    addSuffix: true,
                  })}
                </span>
              )}
            </div>
          </div>
          <RefreshButton playlistId={playlistId} />
        </div>

        <Separator className="mb-6" />

        {/* Active Videos */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle2 className="h-5 w-5 text-green-500" />
            <h2 className="text-xl font-semibold">Active Videos</h2>
            <span className="text-sm text-muted-foreground">
              ({activeVideos.length})
            </span>
          </div>
          <VideoTable videos={activeVideos} />
        </section>

        {/* Removed Videos */}
        {removedVideos.length > 0 && (
          <section>
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="h-5 w-5 text-destructive" />
              <h2 className="text-xl font-semibold">Removed Videos</h2>
              <span className="text-sm text-muted-foreground">
                ({removedVideos.length})
              </span>
            </div>
            <VideoTable videos={removedVideos} showRemovedAt />
          </section>
        )}
      </div>
    </main>
  );
}
