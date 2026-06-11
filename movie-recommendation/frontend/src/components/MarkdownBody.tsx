import type { Components } from "react-markdown"
import ReactMarkdown from "react-markdown"

export type MarkdownBodySize = "compact" | "comfortable"

function markdownComponentsForSize(size: MarkdownBodySize): Components {
  const body =
    size === "comfortable"
      ? "text-base leading-relaxed text-inherit"
      : "text-sm leading-relaxed text-inherit"
  const list = size === "comfortable" ? "text-base text-inherit" : "text-sm text-inherit"
  const h1 =
    size === "comfortable"
      ? "mb-2 mt-3 text-xl font-semibold text-inherit first:mt-0"
      : "mb-2 mt-3 text-base font-semibold text-inherit first:mt-0"
  const h2 =
    size === "comfortable"
      ? "mb-2 mt-3 text-lg font-semibold text-inherit first:mt-0"
      : "mb-2 mt-3 text-sm font-semibold text-inherit first:mt-0"
  const h3 =
    size === "comfortable"
      ? "mb-1.5 mt-2 text-base font-medium text-inherit first:mt-0"
      : "mb-1.5 mt-2 text-sm font-medium text-inherit first:mt-0"
  const codeSm = "text-xs"
  const preSm = "text-xs"

  return {
    p: ({ children }) => <p className={`mb-2 last:mb-0 ${body}`}>{children}</p>,
    h1: ({ children }) => <h1 className={h1}>{children}</h1>,
    h2: ({ children }) => <h2 className={h2}>{children}</h2>,
    h3: ({ children }) => <h3 className={h3}>{children}</h3>,
    ul: ({ children }) => (
      <ul className={`mb-2 list-disc space-y-0.5 pl-5 ${list}`}>{children}</ul>
    ),
    ol: ({ children }) => (
      <ol className={`mb-2 list-decimal space-y-0.5 pl-5 ${list}`}>{children}</ol>
    ),
    li: ({ children }) => <li className="leading-relaxed">{children}</li>,
    strong: ({ children }) => (
      <strong className="font-semibold text-inherit">{children}</strong>
    ),
    a: ({ href, children }) => (
      <a
        href={href}
        className="font-medium text-emerald underline decoration-emerald/50 underline-offset-2 hover:text-emerald-light"
        target="_blank"
        rel="noopener noreferrer"
      >
        {children}
      </a>
    ),
    code: (props) => {
      const { className, children, ...rest } = props
      const isInline = !className
      if (isInline) {
        return (
          <code
            className={`rounded bg-muted px-1 py-0.5 font-mono ${codeSm} text-cream`}
            {...rest}
          >
            {children}
          </code>
        )
      }
      return (
        <code className={className} {...rest}>
          {children}
        </code>
      )
    },
    pre: ({ children }) => (
      <pre
        className={`mb-2 overflow-x-auto rounded-md border border-border bg-surface p-2.5 ${preSm} text-inherit`}
      >
        {children}
      </pre>
    ),
    blockquote: ({ children }) => (
      <blockquote className="mb-2 border-l-2 border-beige/30 pl-3 italic opacity-90">
        {children}
      </blockquote>
    ),
    hr: () => <hr className="my-3 border-border" />,
  }
}

type MarkdownBodyProps = {
  content: string
  className?: string
  size?: MarkdownBodySize
}

export function MarkdownBody({
  content,
  className = "",
  size = "compact",
}: MarkdownBodyProps) {
  const components = markdownComponentsForSize(size)
  return (
    <div className={`min-w-0 ${className}`.trim()}>
      <ReactMarkdown components={components}>{content}</ReactMarkdown>
    </div>
  )
}
