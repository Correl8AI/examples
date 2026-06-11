import { AssistantAvatar } from "@/components/chat/AssistantAvatar"
import {
  ASSISTANT_NAME,
  ASSISTANT_SUBTITLE,
} from "@/components/chat/assistant"
import { cn } from "@/lib/utils"

type AssistantIntroProps = {
  avatarClassName?: string
  className?: string
  size?: "landing" | "chat"
  layout?: "center" | "header"
}

export function AssistantIntro({
  avatarClassName,
  className,
  size = "landing",
  layout = "center",
}: AssistantIntroProps) {
  const isLanding = size === "landing"
  const isHeader = layout === "header" && !isLanding

  return (
    <div
      className={cn(
        "flex flex-col items-center text-center",
        isLanding ? "gap-5" : isHeader ? "gap-2" : "gap-2",
        className
      )}
    >
      <AssistantAvatar
        className={cn(
          "shrink-0 rounded-full object-cover ring-2 ring-beige/20 ring-offset-2 ring-offset-background",
          isLanding
            ? "h-56 w-56 shadow-[0_16px_48px_rgb(0_0_0_0.35),0_0_60px_rgb(212_180_131_0.14)] md:h-64 md:w-64"
            : isHeader
              ? "h-16 w-16 shadow-[0_8px_24px_rgb(0_0_0_0.28),0_0_24px_rgb(212_180_131_0.1)] md:h-20 md:w-20"
              : "h-28 w-28 shadow-[0_12px_32px_rgb(0_0_0_0.3),0_0_40px_rgb(212_180_131_0.12)] md:h-32 md:w-32",
          avatarClassName
        )}
      />
      <div className={cn("min-w-0 space-y-0.5", isLanding && "max-w-sm")}>
        <h1
          className={cn(
            "font-serif font-medium tracking-tight text-cream",
            isLanding
              ? "text-3xl md:text-4xl"
              : isHeader
                ? "text-lg md:text-xl"
                : "text-xl md:text-2xl"
          )}
        >
          {ASSISTANT_NAME}
        </h1>
        {!isHeader && (
          <p
            className={cn(
              "text-muted-foreground",
              isLanding ? "text-base" : "text-sm"
            )}
          >
            {ASSISTANT_SUBTITLE}
          </p>
        )}
      </div>
    </div>
  )
}
