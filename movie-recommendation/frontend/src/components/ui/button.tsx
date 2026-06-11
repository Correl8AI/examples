import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-sm font-medium cinema-transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold/40 disabled:pointer-events-none disabled:opacity-40",
  {
    variants: {
      variant: {
        default:
          "border border-emerald/40 bg-emerald/25 text-cream hover:border-emerald/55 hover:bg-emerald/35 hover:shadow-[0_0_24px_rgb(125_184_150_0.2)]",
        outline:
          "border border-border bg-surface text-cream backdrop-blur-sm hover:border-beige/30 hover:bg-surface-raised",
        secondary:
          "border border-burgundy/40 bg-burgundy/22 text-cream hover:border-burgundy/50 hover:bg-burgundy/32",
        ghost:
          "border border-transparent text-gold-muted hover:border-beige/20 hover:bg-beige/10 hover:text-cream",
      },
      size: {
        default: "h-10 px-5 py-2",
        sm: "h-9 rounded-lg px-4 text-xs",
        icon: "h-11 w-11 rounded-full",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
