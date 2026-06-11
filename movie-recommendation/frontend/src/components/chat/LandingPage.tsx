import { AssistantIntro } from "@/components/chat/AssistantIntro"
import { ChatComposer } from "@/components/chat/ChatComposer"

type LandingPageProps = {
  disabled?: boolean
  error?: string | null
  onSend: (text: string) => void
}

export function LandingPage({ disabled, error, onSend }: LandingPageProps) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-10 px-6 py-12 cinema-fade-in">
      <AssistantIntro size="landing" />
      <ChatComposer variant="landing" disabled={disabled} onSend={onSend} />
      {error && (
        <p className="max-w-lg text-center text-sm text-burgundy-light">{error}</p>
      )}
    </div>
  )
}
