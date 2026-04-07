"use client";

import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { RefreshCw, Trash2, ListVideo, AlertTriangle } from "lucide-react";
import { refreshPlaylist, deletePlaylist } from "@/app/actions/youtube";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { useTransition } from "react";
import { formatDistanceToNow } from "date-fns";

interface PlaylistCardProps {
  id: string;
  name: string;
  description: string | null;
  channelName: string | null;
  activeCount: number;
  removedCount: number;
  lastFetched: string | null;
}

export function PlaylistCard({
  id,
  name,
  description,
  channelName,
  activeCount,
  removedCount,
  lastFetched,
}: PlaylistCardProps) {
  const router = useRouter();
  const [isRefreshing, startRefresh] = useTransition();
  const [isDeleting, startDelete] = useTransition();

  function handleRefresh(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    startRefresh(async () => {
      const result = await refreshPlaylist(id);
      if (result.success) {
        toast.success(result.message);
        router.refresh();
      } else {
        toast.error(result.message);
      }
    });
  }

  function handleDelete(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    startDelete(async () => {
      const result = await deletePlaylist(id);
      if (result.success) {
        toast.success(result.message);
        router.refresh();
      } else {
        toast.error(result.message);
      }
    });
  }

  return (
    <Link href={`/${id}`}>
      <Card className="group hover:border-primary/30 transition-all duration-200 hover:shadow-lg hover:shadow-primary/5 cursor-pointer">
        <CardContent className="p-5">
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-lg truncate group-hover:text-primary transition-colors">
                {name}
              </h3>
              {channelName && (
                <p className="text-sm text-muted-foreground mt-0.5">
                  {channelName}
                </p>
              )}
              {description && (
                <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
                  {description}
                </p>
              )}
            </div>
            <ListVideo className="h-8 w-8 text-muted-foreground/50 shrink-0" />
          </div>

          <div className="flex items-center gap-2 mt-4 flex-wrap">
            <Badge variant="secondary">
              {activeCount} video{activeCount !== 1 ? "s" : ""}
            </Badge>
            {removedCount > 0 && (
              <Badge variant="destructive" className="gap-1">
                <AlertTriangle className="h-3 w-3" />
                {removedCount} removed
              </Badge>
            )}
            {lastFetched && (
              <span className="text-xs text-muted-foreground ml-auto">
                Updated{" "}
                {formatDistanceToNow(new Date(lastFetched), {
                  addSuffix: true,
                })}
              </span>
            )}
          </div>

          <div className="flex gap-2 mt-4">
            <Button
              variant="outline"
              size="sm"
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="gap-1.5"
            >
              <RefreshCw
                className={`h-3.5 w-3.5 ${isRefreshing ? "animate-spin" : ""}`}
              />
              Refresh
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleDelete}
              disabled={isDeleting}
              className="gap-1.5 text-muted-foreground hover:text-destructive"
            >
              <Trash2 className="h-3.5 w-3.5" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
