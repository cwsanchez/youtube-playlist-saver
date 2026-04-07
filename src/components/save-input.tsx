"use client";

import { useState, useTransition } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader2, Plus } from "lucide-react";
import { savePlaylistOrVideo } from "@/app/actions/youtube";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

export function SaveInput() {
  const [url, setUrl] = useState("");
  const [isPending, startTransition] = useTransition();
  const router = useRouter();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!url.trim()) {
      toast.error("Please enter a YouTube URL or ID.");
      return;
    }
    startTransition(async () => {
      const result = await savePlaylistOrVideo(url.trim());
      if (result.success) {
        toast.success(result.message);
        setUrl("");
        router.refresh();
        if (result.type === "playlist" && result.id) {
          router.push(`/${result.id}`);
        }
      } else {
        toast.error(result.message);
      }
    });
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-3 w-full max-w-2xl">
      <Input
        type="text"
        placeholder="Paste YouTube playlist or video URL..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        disabled={isPending}
        className="flex-1 h-12 text-base bg-card border-border"
      />
      <Button
        type="submit"
        disabled={isPending}
        size="lg"
        className="h-12 px-6"
      >
        {isPending ? (
          <Loader2 className="h-5 w-5 animate-spin" />
        ) : (
          <>
            <Plus className="h-5 w-5 mr-2" />
            Save
          </>
        )}
      </Button>
    </form>
  );
}
