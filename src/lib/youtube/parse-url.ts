import type { ParsedInput } from "./types";

const PLAYLIST_ID_PATTERNS = [
  /[?&]list=([a-zA-Z0-9_-]+)/,
  /^(PL[a-zA-Z0-9_-]+)$/,
  /^(UU[a-zA-Z0-9_-]+)$/,
  /^(FL[a-zA-Z0-9_-]+)$/,
  /^(OL[a-zA-Z0-9_-]+)$/,
  /^(RD[a-zA-Z0-9_-]+)$/,
  /^(LL[a-zA-Z0-9_-]+)$/,
];

const VIDEO_ID_PATTERNS = [
  /(?:youtube\.com\/watch\?.*v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})/,
  /^([a-zA-Z0-9_-]{11})$/,
];

export function parseYouTubeInput(input: string): ParsedInput {
  const trimmed = input.trim();

  for (const pattern of PLAYLIST_ID_PATTERNS) {
    const match = trimmed.match(pattern);
    if (match) {
      return { type: "playlist", id: match[1] };
    }
  }

  for (const pattern of VIDEO_ID_PATTERNS) {
    const match = trimmed.match(pattern);
    if (match) {
      return { type: "video", id: match[1] };
    }
  }

  return { type: "unknown", id: trimmed };
}

export function extractPlaylistId(url: string): string | null {
  const match = url.match(/[?&]list=([a-zA-Z0-9_-]+)/);
  if (match) return match[1];

  for (const pattern of PLAYLIST_ID_PATTERNS) {
    const m = url.trim().match(pattern);
    if (m) return m[1];
  }

  return null;
}

export function extractVideoId(url: string): string | null {
  for (const pattern of VIDEO_ID_PATTERNS) {
    const match = url.trim().match(pattern);
    if (match) return match[1];
  }
  return null;
}
