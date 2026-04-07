"use client";

import { Button } from "@/components/ui/button";
import { RefreshCw } from "lucide-react";
import { refreshPlaylist } from "@/app/actions/youtube";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { useTransition } from "react";

export function RefreshButton({ playlistId }: { playlistId: string }) {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();

  function handleClick() {
    startTransition(async () => {
      const result = await refreshPlaylist(playlistId);
      if (result.success) {
        toast.success(result.message);
        router.refresh();
      } else {
        toast.error(result.message);
      }
    });
  }

  return (
    <Button
      onClick={handleClick}
      disabled={isPending}
      variant="outline"
      className="gap-2"
    >
      <RefreshCw className={`h-4 w-4 ${isPending ? "animate-spin" : ""}`} />
      {isPending ? "Refreshing..." : "Refresh Playlist"}
    </Button>
  );
}
