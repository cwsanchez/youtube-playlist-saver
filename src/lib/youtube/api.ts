import type {
  YouTubePlaylistResponse,
  YouTubePlaylistItemsResponse,
  YouTubeVideosResponse,
  YouTubeChannelResponse,
  YouTubeErrorResponse,
} from "./types";

const YT_API_BASE = "https://www.googleapis.com/youtube/v3";

function getApiKey(): string {
  const key = process.env.YOUTUBE_API_KEY;
  if (!key) throw new Error("Missing YOUTUBE_API_KEY environment variable");
  return key;
}

function buildParams(
  parts: string[],
  extra: Record<string, string | number | undefined>
): URLSearchParams {
  const params = new URLSearchParams();
  params.set("part", parts.join(","));
  params.set("key", getApiKey());
  for (const [k, v] of Object.entries(extra)) {
    if (v !== undefined) params.set(k, String(v));
  }
  return params;
}

async function ytFetch<T>(endpoint: string, params: URLSearchParams): Promise<T> {
  const url = `${YT_API_BASE}/${endpoint}?${params.toString()}`;
  const res = await fetch(url, {
    headers: { Accept: "application/json" },
    next: { revalidate: 0 },
  });

  const data = await res.json();

  if ("error" in data) {
    const err = data as YouTubeErrorResponse;
    const msg = err.error.message || "Unknown YouTube API error";
    const code = err.error.code;
    if (code === 403 && msg.toLowerCase().includes("quota")) {
      throw new Error(
        "YouTube API quota exceeded. Please wait or increase your quota."
      );
    }
    throw new Error(`YouTube API error (${code}): ${msg}`);
  }

  return data as T;
}

export async function fetchPlaylist(playlistId: string): Promise<YouTubePlaylistResponse> {
  const params = buildParams(["snippet", "contentDetails"], { id: playlistId });
  return ytFetch<YouTubePlaylistResponse>("playlists", params);
}

export async function fetchPlaylistVideoIds(playlistId: string): Promise<string[]> {
  const allIds: string[] = [];
  let pageToken: string | undefined;

  do {
    const params = buildParams(["contentDetails"], {
      playlistId,
      maxResults: 50,
      pageToken,
    });
    const data = await ytFetch<YouTubePlaylistItemsResponse>("playlistItems", params);

    for (const item of data.items) {
      if (item.kind === "youtube#playlistItem") {
        allIds.push(item.contentDetails.videoId);
      }
    }
    pageToken = data.nextPageToken;
  } while (pageToken);

  return allIds;
}

function chunks<T>(arr: T[], size: number): T[][] {
  const result: T[][] = [];
  for (let i = 0; i < arr.length; i += size) {
    result.push(arr.slice(i, i + size));
  }
  return result;
}

export async function fetchVideos(videoIds: string[]): Promise<YouTubeVideosResponse> {
  if (videoIds.length === 0) return { kind: "", etag: "", pageInfo: { totalResults: 0, resultsPerPage: 0 }, items: [] };

  const allItems: YouTubeVideosResponse["items"] = [];

  for (const chunk of chunks(videoIds, 50)) {
    const params = buildParams(["snippet", "contentDetails", "statistics"], {
      id: chunk.join(","),
      maxResults: 50,
    });
    const data = await ytFetch<YouTubeVideosResponse>("videos", params);
    allItems.push(...data.items);
  }

  return {
    kind: "youtube#videoListResponse",
    etag: "",
    pageInfo: { totalResults: allItems.length, resultsPerPage: 50 },
    items: allItems,
  };
}

export async function fetchChannel(channelId: string): Promise<YouTubeChannelResponse> {
  const params = buildParams(["snippet"], { id: channelId });
  return ytFetch<YouTubeChannelResponse>("channels", params);
}

export async function fetchSingleVideo(videoId: string): Promise<YouTubeVideosResponse> {
  return fetchVideos([videoId]);
}
