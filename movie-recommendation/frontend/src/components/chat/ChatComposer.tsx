import { useState } from "react"

import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { cn } from "@/lib/utils"

type ChatComposerProps = {
  disabled?: boolean
  onSend: (text: string) => void
  variant?: "landing" | "chat"
}

export function ChatComposer({
  disabled,
  onSend,
  variant = "chat",
}: ChatComposerProps) {
  const [value, setValue] = useState("")

  function submit() {
    const text = value.trim()
    if (!text || disabled) return
    onSend(text)
    setValue("")
  }

  const isLanding = variant === "landing"

  const composer = (
    <div className="flex flex-col gap-0 overflow-hidden rounded-2xl border border-border bg-input shadow-[0_4px_20px_rgb(0_0_0_0.08),inset_0_1px_0_rgb(245_240_232_0.12)] backdrop-blur-xl">
      <Textarea
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder={
          isLanding
            ? "What shall we watch?"
            : "Describe the evening you have in mind…"
        }
        disabled={disabled}
        rows={isLanding ? 1 : 2}
        className={cn(
          "min-h-[44px] resize-none rounded-none border-0 bg-transparent px-3 pb-0.5 pt-2.5 shadow-none backdrop-blur-none focus-visible:border-transparent focus-visible:ring-0",
          isLanding ? "min-h-[48px] text-base" : "text-sm"
        )}
        onKeyDown={(event) => {
          if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault()
            submit()
          }
        }}
      />
      <div
        className="flex w-full items-center gap-1.5 bg-transparent px-2 pb-2 pt-0"
        role="toolbar"
        aria-label="Message actions"
      >
        <span className="min-w-0 flex-1" aria-hidden />
        <Button
          type="button"
          variant="ghost"
          size="sm"
          disabled={disabled || !value.trim()}
          onClick={submit}
          className="text-emerald hover:bg-beige/10 hover:text-emerald-light"
        >
          Send
        </Button>
      </div>
    </div>
  )

  if (isLanding) {
    return (
      <div className="w-full max-w-lg px-4 cinema-transition">{composer}</div>
    )
  }

  return (
    <div className="w-full shrink-0 border-t border-border px-0 pb-3 pt-2 cinema-transition">
      <div className="mx-auto w-full max-w-3xl">{composer}</div>
    </div>
  )
}
