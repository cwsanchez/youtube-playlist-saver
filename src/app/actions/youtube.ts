"use server";

import { createServerClient } from "@/lib/supabase/server";
import {
  fetchPlaylist,
  fetchPlaylistVideoIds,
  fetchVideos,
  fetchChannel,
  fetchSingleVideo,
} from "@/lib/youtube/api";
import { parseYouTubeInput } from "@/lib/youtube/parse-url";
import type { YouTubeVideoItem } from "@/lib/youtube/types";
import { revalidatePath } from "next/cache";

function bestThumbnail(
  thumbnails: YouTubeVideoItem["snippet"]["thumbnails"]
): string | null {
  return (
    thumbnails.maxres?.url ??
    thumbnails.standard?.url ??
    thumbnails.high?.url ??
    thumbnails.medium?.url ??
    thumbnails.default?.url ??
    null
  );
}

async function upsertChannel(channelId: string, channelName: string) {
  const supabase = createServerClient();
  await supabase.from("channels").upsert(
    { id: channelId, name: channelName },
    { onConflict: "id" }
  );
}

async function upsertVideos(videos: YouTubeVideoItem[]) {
  if (videos.length === 0) return;
  const supabase = createServerClient();

  const uniqueChannels = new Map<string, string>();
  for (const v of videos) {
    uniqueChannels.set(v.snippet.channelId, v.snippet.channelTitle);
  }

  for (const [cid, cname] of uniqueChannels) {
    await upsertChannel(cid, cname);
  }

  const rows = videos.map((v) => ({
    id: v.id,
    name: v.snippet.title,
    description: v.snippet.description,
    channel_id: v.snippet.channelId,
    thumbnail_url: bestThumbnail(v.snippet.thumbnails),
    published_at: v.snippet.publishedAt,
    view_count: v.statistics?.viewCount
      ? parseInt(v.statistics.viewCount, 10)
      : null,
    like_count: v.statistics?.likeCount
      ? parseInt(v.statistics.likeCount, 10)
      : null,
    duration: v.contentDetails?.duration ?? null,
  }));

  const chunkSize = 100;
  for (let i = 0; i < rows.length; i += chunkSize) {
    const chunk = rows.slice(i, i + chunkSize);
    const { error } = await supabase
      .from("videos")
      .upsert(chunk, { onConflict: "id" });
    if (error) throw new Error(`Failed to upsert videos: ${error.message}`);
  }
}

export async function savePlaylistOrVideo(
  url: string
): Promise<{ success: boolean; message: string; id?: string; type?: string }> {
  try {
    const parsed = parseYouTubeInput(url);

    if (parsed.type === "unknown") {
      return {
        success: false,
        message:
          "Could not detect a valid YouTube playlist or video URL/ID. Please check the input.",
      };
    }

    if (parsed.type === "video") {
      return await saveVideo(parsed.id);
    }

    return await savePlaylist(parsed.id);
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Unknown error occurred";
    return { success: false, message: msg };
  }
}

async function saveVideo(
  videoId: string
): Promise<{ success: boolean; message: string; id?: string; type?: string }> {
  const videoData = await fetchSingleVideo(videoId);

  if (videoData.items.length === 0) {
    return { success: false, message: "Video not found or is private." };
  }

  await upsertVideos(videoData.items);

  return {
    success: true,
    message: `Video "${videoData.items[0].snippet.title}" saved successfully.`,
    id: videoId,
    type: "video",
  };
}

async function savePlaylist(
  playlistId: string
): Promise<{ success: boolean; message: string; id?: string; type?: string }> {
  const supabase = createServerClient();

  const playlistData = await fetchPlaylist(playlistId);
  if (playlistData.items.length === 0) {
    return { success: false, message: "Playlist not found or is private." };
  }

  const plItem = playlistData.items[0];
  const channelId = plItem.snippet.channelId;

  const channelData = await fetchChannel(channelId);
  if (channelData.items.length > 0) {
    await upsertChannel(channelData.items[0].id, channelData.items[0].snippet.title);
  }

  const { error: plError } = await supabase.from("playlists").upsert(
    {
      id: plItem.id,
      name: plItem.snippet.title,
      description: plItem.snippet.description,
      channel_id: channelId,
      last_fetched: new Date().toISOString(),
    },
    { onConflict: "id" }
  );
  if (plError) throw new Error(`Failed to upsert playlist: ${plError.message}`);

  const videoIds = await fetchPlaylistVideoIds(playlistId);
  const videosData = await fetchVideos(videoIds);
  await upsertVideos(videosData.items);

  const fetchedVideoIds = new Set(videosData.items.map((v) => v.id));

  for (const vid of fetchedVideoIds) {
    await supabase.from("playlists_videos").upsert(
      { playlist_id: playlistId, video_id: vid, removed_at: null },
      { onConflict: "playlist_id,video_id" }
    );
  }

  revalidatePath("/");
  revalidatePath(`/${playlistId}`);

  return {
    success: true,
    message: `Playlist "${plItem.snippet.title}" saved with ${fetchedVideoIds.size} videos.`,
    id: playlistId,
    type: "playlist",
  };
}

export async function refreshPlaylist(
  playlistId: string
): Promise<{ success: boolean; message: string }> {
  try {
    const supabase = createServerClient();

    const videoIds = await fetchPlaylistVideoIds(playlistId);
    const videosData = await fetchVideos(videoIds);
    await upsertVideos(videosData.items);

    const currentVideoIds = new Set(videosData.items.map((v) => v.id));

    const { data: existingLinks } = await supabase
      .from("playlists_videos")
      .select("video_id, removed_at")
      .eq("playlist_id", playlistId);

    const existingMap = new Map(
      (existingLinks ?? []).map((l) => [l.video_id, l.removed_at])
    );

    for (const vid of currentVideoIds) {
      if (!existingMap.has(vid)) {
        await supabase
          .from("playlists_videos")
          .insert({ playlist_id: playlistId, video_id: vid, removed_at: null });
      } else if (existingMap.get(vid) !== null) {
        await supabase
          .from("playlists_videos")
          .update({ removed_at: null })
          .eq("playlist_id", playlistId)
          .eq("video_id", vid);
      }
    }

    let removedCount = 0;
    for (const [vid, removedAt] of existingMap) {
      if (!currentVideoIds.has(vid) && removedAt === null) {
        await supabase
          .from("playlists_videos")
          .update({ removed_at: new Date().toISOString() })
          .eq("playlist_id", playlistId)
          .eq("video_id", vid);
        removedCount++;
      }
    }

    await supabase
      .from("playlists")
      .update({ last_fetched: new Date().toISOString() })
      .eq("id", playlistId);

    revalidatePath("/");
    revalidatePath(`/${playlistId}`);

    return {
      success: true,
      message: `Refreshed playlist. ${currentVideoIds.size} active videos.${
        removedCount > 0 ? ` ${removedCount} videos marked as removed.` : ""
      }`,
    };
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Unknown error occurred";
    return { success: false, message: msg };
  }
}

export async function getPlaylists() {
  const supabase = createServerClient();

  const { data: playlists, error } = await supabase
    .from("playlists")
    .select("*, channels(name)")
    .order("created_at", { ascending: false });

  if (error) throw new Error(error.message);

  const playlistsWithCounts = await Promise.all(
    (playlists ?? []).map(async (pl) => {
      const { count: activeCount } = await supabase
        .from("playlists_videos")
        .select("*", { count: "exact", head: true })
        .eq("playlist_id", pl.id)
        .is("removed_at", null);

      const { count: removedCount } = await supabase
        .from("playlists_videos")
        .select("*", { count: "exact", head: true })
        .eq("playlist_id", pl.id)
        .not("removed_at", "is", null);

      return {
        ...pl,
        active_count: activeCount ?? 0,
        removed_count: removedCount ?? 0,
        video_count: (activeCount ?? 0) + (removedCount ?? 0),
      };
    })
  );

  return playlistsWithCounts;
}

interface VideoRow {
  id: string;
  name: string;
  description: string | null;
  thumbnail_url: string | null;
  published_at: string | null;
  view_count: number | null;
  like_count: number | null;
  duration: string | null;
  removed_at?: string | null;
}

export async function getPlaylistDetail(playlistId: string) {
  const supabase = createServerClient();

  const { data: playlist } = await supabase
    .from("playlists")
    .select("*, channels(name)")
    .eq("id", playlistId)
    .single();

  if (!playlist) return null;

  const { data: activeRows } = await supabase
    .from("playlists_videos")
    .select("video_id, removed_at, videos(*)")
    .eq("playlist_id", playlistId)
    .is("removed_at", null)
    .order("video_id");

  const { data: removedRows } = await supabase
    .from("playlists_videos")
    .select("video_id, removed_at, videos(*)")
    .eq("playlist_id", playlistId)
    .not("removed_at", "is", null)
    .order("removed_at", { ascending: false });

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  function toVideoRow(row: any): VideoRow {
    const v = row.videos ?? {};
    return {
      id: v.id ?? row.video_id,
      name: v.name ?? "",
      description: v.description ?? null,
      thumbnail_url: v.thumbnail_url ?? null,
      published_at: v.published_at ?? null,
      view_count: v.view_count ?? null,
      like_count: v.like_count ?? null,
      duration: v.duration ?? null,
      removed_at: row.removed_at,
    };
  }

  return {
    playlist,
    activeVideos: (activeRows ?? []).map(toVideoRow),
    removedVideos: (removedRows ?? []).map(toVideoRow),
  };
}

export async function deletePlaylist(
  playlistId: string
): Promise<{ success: boolean; message: string }> {
  try {
    const supabase = createServerClient();

    await supabase
      .from("playlists_videos")
      .delete()
      .eq("playlist_id", playlistId);

    await supabase.from("playlists").delete().eq("id", playlistId);

    revalidatePath("/");

    return { success: true, message: "Playlist deleted." };
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Unknown error";
    return { success: false, message: msg };
  }
}
