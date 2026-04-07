export interface YouTubePageInfo {
  totalResults: number;
  resultsPerPage: number;
}

export interface YouTubeThumbnail {
  url: string;
  width: number;
  height: number;
}

export interface YouTubeThumbnails {
  default?: YouTubeThumbnail;
  medium?: YouTubeThumbnail;
  high?: YouTubeThumbnail;
  standard?: YouTubeThumbnail;
  maxres?: YouTubeThumbnail;
}

export interface YouTubePlaylistSnippet {
  publishedAt: string;
  channelId: string;
  title: string;
  description: string;
  thumbnails: YouTubeThumbnails;
  channelTitle: string;
}

export interface YouTubePlaylistItem {
  kind: string;
  etag: string;
  id: string;
  snippet: YouTubePlaylistSnippet;
  contentDetails: {
    itemCount: number;
  };
}

export interface YouTubePlaylistResponse {
  kind: string;
  etag: string;
  pageInfo: YouTubePageInfo;
  items: YouTubePlaylistItem[];
}

export interface YouTubePlaylistItemSnippet {
  publishedAt: string;
  channelId: string;
  title: string;
  description: string;
  thumbnails: YouTubeThumbnails;
  channelTitle: string;
  playlistId: string;
  position: number;
  resourceId: {
    kind: string;
    videoId: string;
  };
}

export interface YouTubePlaylistItemItem {
  kind: string;
  etag: string;
  id: string;
  contentDetails: {
    videoId: string;
    videoPublishedAt?: string;
  };
}

export interface YouTubePlaylistItemsResponse {
  kind: string;
  etag: string;
  nextPageToken?: string;
  pageInfo: YouTubePageInfo;
  items: YouTubePlaylistItemItem[];
}

export interface YouTubeVideoSnippet {
  publishedAt: string;
  channelId: string;
  title: string;
  description: string;
  thumbnails: YouTubeThumbnails;
  channelTitle: string;
  tags?: string[];
  categoryId: string;
}

export interface YouTubeVideoStatistics {
  viewCount?: string;
  likeCount?: string;
  favoriteCount?: string;
  commentCount?: string;
}

export interface YouTubeVideoContentDetails {
  duration: string;
  dimension: string;
  definition: string;
  caption: string;
}

export interface YouTubeVideoItem {
  kind: string;
  etag: string;
  id: string;
  snippet: YouTubeVideoSnippet;
  contentDetails: YouTubeVideoContentDetails;
  statistics: YouTubeVideoStatistics;
}

export interface YouTubeVideosResponse {
  kind: string;
  etag: string;
  pageInfo: YouTubePageInfo;
  items: YouTubeVideoItem[];
}

export interface YouTubeChannelSnippet {
  title: string;
  description: string;
  thumbnails: YouTubeThumbnails;
}

export interface YouTubeChannelItem {
  kind: string;
  etag: string;
  id: string;
  snippet: YouTubeChannelSnippet;
}

export interface YouTubeChannelResponse {
  kind: string;
  etag: string;
  pageInfo: YouTubePageInfo;
  items: YouTubeChannelItem[];
}

export interface YouTubeErrorResponse {
  error: {
    code: number;
    message: string;
    errors: Array<{ message: string; domain: string; reason: string }>;
  };
}

// Database types
export interface Channel {
  id: string;
  name: string;
  created_at?: string;
}

export interface Playlist {
  id: string;
  name: string;
  description: string | null;
  channel_id: string | null;
  last_fetched: string | null;
  created_at?: string;
}

export interface Video {
  id: string;
  name: string;
  description: string | null;
  channel_id: string | null;
  thumbnail_url: string | null;
  published_at: string | null;
  view_count: number | null;
  like_count: number | null;
  duration: string | null;
  created_at?: string;
}

export interface PlaylistVideo {
  playlist_id: string;
  video_id: string;
  removed_at: string | null;
}

export interface PlaylistWithDetails extends Playlist {
  channels?: Channel | null;
  video_count?: number;
  active_count?: number;
  removed_count?: number;
}

export interface VideoWithStatus extends Video {
  removed_at?: string | null;
}

export type InputType = "playlist" | "video" | "unknown";

export interface ParsedInput {
  type: InputType;
  id: string;
}
