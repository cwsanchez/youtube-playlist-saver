"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import { PlaylistCard } from "./playlist-card";

interface PlaylistItem {
  id: string;
  name: string;
  description: string | null;
  channel_id: string | null;
  channels: { name: string } | null;
  active_count: number;
  removed_count: number;
  last_fetched: string | null;
}

export function PlaylistSearch({ playlists }: { playlists: PlaylistItem[] }) {
  const [query, setQuery] = useState("");

  const filtered = playlists.filter(
    (pl) =>
      pl.name.toLowerCase().includes(query.toLowerCase()) ||
      (pl.channels?.name ?? "").toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div>
      <div className="flex items-center gap-3 mb-6">
        <h2 className="text-xl font-semibold">
          Saved Playlists
        </h2>
        <span className="text-sm text-muted-foreground">
          ({playlists.length})
        </span>
        {playlists.length > 3 && (
          <div className="relative ml-auto w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search playlists..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="pl-9 h-9"
            />
          </div>
        )}
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {filtered.map((pl) => (
          <PlaylistCard
            key={pl.id}
            id={pl.id}
            name={pl.name}
            description={pl.description}
            channelName={pl.channels?.name ?? null}
            activeCount={pl.active_count}
            removedCount={pl.removed_count}
            lastFetched={pl.last_fetched}
          />
        ))}
      </div>

      {query && filtered.length === 0 && (
        <p className="text-center text-muted-foreground py-8">
          No playlists match &ldquo;{query}&rdquo;
        </p>
      )}
    </div>
  );
}
