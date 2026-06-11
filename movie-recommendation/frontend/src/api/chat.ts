export type ChatRole = "user" | "assistant"

export type ChatMessage = {
  role: ChatRole
  content: string
}

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8001"

export async function postChat(
  messages: ChatMessage[],
  interactionId: string,
  userId = "demo-user"
): Promise<ChatMessage> {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      messages,
      interaction_id: interactionId,
      user_id: userId,
    }),
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(detail || `Request failed (${response.status})`)
  }

  const data = (await response.json()) as { message: ChatMessage }
  return data.message
}
