import { useMemo, useState } from "react"

import { postChat, type ChatMessage } from "@/api/chat"
import { AssistantIntro } from "@/components/chat/AssistantIntro"
import { ChatComposer } from "@/components/chat/ChatComposer"
import { LandingPage } from "@/components/chat/LandingPage"
import { MessageList } from "@/components/chat/MessageList"

function createInteractionId() {
  return crypto.randomUUID()
}

export default function App() {
  const interactionId = useMemo(() => createInteractionId(), [])
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const chatStarted = messages.length > 0 || loading

  async function send(text: string) {
    const nextMessages: ChatMessage[] = [
      ...messages,
      { role: "user", content: text },
    ]
    setMessages(nextMessages)
    setLoading(true)
    setError(null)

    try {
      const reply = await postChat(nextMessages, interactionId)
      setMessages((current) => [...current, reply])
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong")
    } finally {
      setLoading(false)
    }
  }

  if (!chatStarted) {
    return <LandingPage disabled={loading} error={error} onSend={send} />
  }

  return (
    <div className="flex h-screen flex-col px-4 py-3 cinema-fade-in">
      <div className="mx-auto flex w-full max-w-3xl shrink-0 justify-center pb-2 pt-1">
        <AssistantIntro size="chat" layout="header" />
      </div>
      <div className="flex min-h-0 flex-1 flex-col">
        <MessageList messages={messages} loading={loading} />
        {error && (
          <p className="mx-auto w-full max-w-3xl pb-2 text-sm text-burgundy-light">
            {error}
          </p>
        )}
        <ChatComposer disabled={loading} onSend={send} />
      </div>
    </div>
  )
}
