import { useEffect, useRef } from "react"

import type { ChatMessage } from "@/api/chat"
import { AssistantMarkdown } from "@/components/chat/AssistantMarkdown"
import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"

type MessageListProps = {
  messages: ChatMessage[]
  loading: boolean
}

function scrollToBottom(container: HTMLDivElement) {
  container.scrollTo({ top: container.scrollHeight, behavior: "smooth" })
}

export function MessageList({ messages, loading }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const container = scrollRef.current
    if (!container) return

    scrollToBottom(container)
    const frame = requestAnimationFrame(() => scrollToBottom(container))
    return () => cancelAnimationFrame(frame)
  }, [messages, loading])

  return (
    <div
      ref={scrollRef}
      className="flex min-h-0 w-full flex-1 flex-col overflow-y-auto py-4"
    >
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-5">
      {messages.map((message, index) => {
        const prev = messages[index - 1]
        const afterUser = message.role === "assistant" && prev?.role === "user"

        return message.role === "user" ? (
          <Card
            key={`${message.role}-${index}`}
            className="w-full gap-0 px-3 py-2.5 text-left text-sm cinema-fade-in"
          >
            <div className="mb-1 text-xs font-medium uppercase tracking-wide text-muted-foreground">
              You
            </div>
            <div className="whitespace-pre-wrap break-words text-cream">
              {message.content}
            </div>
          </Card>
        ) : (
          <div
            key={`${message.role}-${index}`}
            className={cn("w-full text-left cinema-fade-in", afterUser && "mt-4")}
          >
            <AssistantMarkdown content={message.content} />
          </div>
        )
      })}
      {loading && (
        <div
          className="mt-4 w-full py-1 text-left text-sm text-muted-foreground cinema-fade-in"
          aria-busy
          aria-live="polite"
        >
          Thinking…
        </div>
      )}
      </div>
    </div>
  )
}
