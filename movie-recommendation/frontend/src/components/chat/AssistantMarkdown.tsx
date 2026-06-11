import { MarkdownBody } from "@/components/MarkdownBody"
import { cn } from "@/lib/utils"

type AssistantMarkdownProps = {
  content: string
  className?: string
}

export function AssistantMarkdown({ content, className }: AssistantMarkdownProps) {
  return (
    <MarkdownBody
      content={content}
      size="compact"
      className={cn("min-w-0 text-cream", className)}
    />
  )
}
