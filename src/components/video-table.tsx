"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { formatDuration, formatViewCount, truncate } from "@/lib/format";
import { formatDistanceToNow } from "date-fns";
import { ExternalLink, Clock } from "lucide-react";
import Image from "next/image";
import { useState } from "react";

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

const PAGE_SIZE = 25;

export function VideoTable({
  videos,
  showRemovedAt = false,
}: {
  videos: VideoRow[];
  showRemovedAt?: boolean;
}) {
  const [page, setPage] = useState(0);
  const totalPages = Math.ceil(videos.length / PAGE_SIZE);
  const paginated = videos.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  if (videos.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        No videos found.
      </div>
    );
  }

  return (
    <div>
      <div className="rounded-lg border overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead className="w-12 text-center">#</TableHead>
              <TableHead className="w-28">Thumbnail</TableHead>
              <TableHead>Title</TableHead>
              <TableHead className="hidden md:table-cell w-48">
                Description
              </TableHead>
              <TableHead className="w-24 text-center hidden sm:table-cell">
                Published
              </TableHead>
              <TableHead className="w-20 text-center hidden sm:table-cell">
                Views
              </TableHead>
              <TableHead className="w-20 text-center hidden lg:table-cell">
                Duration
              </TableHead>
              {showRemovedAt && (
                <TableHead className="w-28 text-center">Removed</TableHead>
              )}
            </TableRow>
          </TableHeader>
          <TableBody>
            {paginated.map((video, idx) => (
              <TableRow key={video.id} className="group">
                <TableCell className="text-center text-muted-foreground text-sm">
                  {page * PAGE_SIZE + idx + 1}
                </TableCell>
                <TableCell>
                  <a
                    href={`https://www.youtube.com/watch?v=${video.id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block"
                  >
                    {video.thumbnail_url ? (
                      <Image
                        src={video.thumbnail_url}
                        alt={video.name}
                        width={120}
                        height={68}
                        className="w-24 h-auto rounded-md object-cover"
                      />
                    ) : (
                      <div className="w-24 h-14 rounded-md bg-muted flex items-center justify-center text-xs text-muted-foreground">
                        No img
                      </div>
                    )}
                  </a>
                </TableCell>
                <TableCell>
                  <a
                    href={`https://www.youtube.com/watch?v=${video.id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-medium hover:text-primary transition-colors inline-flex items-center gap-1.5 group-hover:underline"
                  >
                    {truncate(video.name, 60)}
                    <ExternalLink className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
                  </a>
                </TableCell>
                <TableCell className="hidden md:table-cell text-sm text-muted-foreground">
                  {truncate(video.description, 80)}
                </TableCell>
                <TableCell className="text-center text-sm text-muted-foreground hidden sm:table-cell">
                  {video.published_at
                    ? formatDistanceToNow(new Date(video.published_at), {
                        addSuffix: true,
                      })
                    : "-"}
                </TableCell>
                <TableCell className="text-center text-sm hidden sm:table-cell">
                  {formatViewCount(video.view_count)}
                </TableCell>
                <TableCell className="text-center text-sm text-muted-foreground hidden lg:table-cell">
                  <span className="inline-flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    {formatDuration(video.duration)}
                  </span>
                </TableCell>
                {showRemovedAt && (
                  <TableCell className="text-center">
                    {video.removed_at ? (
                      <Badge variant="destructive" className="text-xs">
                        {formatDistanceToNow(new Date(video.removed_at), {
                          addSuffix: true,
                        })}
                      </Badge>
                    ) : (
                      "-"
                    )}
                  </TableCell>
                )}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-4">
          <p className="text-sm text-muted-foreground">
            Showing {page * PAGE_SIZE + 1}-
            {Math.min((page + 1) * PAGE_SIZE, videos.length)} of{" "}
            {videos.length}
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setPage((p) => Math.max(0, p - 1))}
              disabled={page === 0}
              className="px-3 py-1 text-sm rounded-md border hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Previous
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
              disabled={page >= totalPages - 1}
              className="px-3 py-1 text-sm rounded-md border hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
