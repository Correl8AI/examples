import * as React from "react"

import { cn } from "@/lib/utils"

const Textarea = React.forwardRef<
  HTMLTextAreaElement,
  React.ComponentProps<"textarea">
>(({ className, ...props }, ref) => {
  return (
    <textarea
      className={cn(
        "flex min-h-[80px] w-full rounded-2xl border border-border bg-input px-4 py-3 text-sm text-cream shadow-[0_4px_20px_rgb(0_0_0_0.08),inset_0_1px_0_rgb(245_240_232_0.1)] backdrop-blur-xl cinema-transition placeholder:text-gold-muted focus-visible:border-emerald/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald/30 disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      ref={ref}
      {...props}
    />
  )
})
Textarea.displayName = "Textarea"

export { Textarea }
