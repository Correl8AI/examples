import assistantAvatar from "@/assets/assistant-avatar.png"

import { ASSISTANT_NAME } from "@/components/chat/assistant"

export function AssistantAvatar({ className }: { className?: string }) {
  return (
    <img
      src={assistantAvatar}
      alt={ASSISTANT_NAME}
      className={className}
    />
  )
}
