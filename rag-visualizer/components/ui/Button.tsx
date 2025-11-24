interface ButtonProps {
  children: React.ReactNode;
  type?: "button" | "submit";
  onClick?: () => void;
  disabled?: boolean;
  isPondering?: boolean;
}

export function Button({
  children,
  type = "button",
  onClick,
  disabled = false,
  isPondering = false,
}: ButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || isPondering}
      className={`w-full rounded-lg px-6 py-3 text-sm font-semibold text-white transition-all focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 focus:ring-offset-background ${
        isPondering
          ? "bg-accent/80 cursor-wait"
          : disabled
            ? "bg-accent/50 cursor-not-allowed"
            : "bg-accent hover:bg-accent-hover"
      }`}
    >
      {isPondering ? (
        <span className="flex items-center justify-center gap-2">
          <span className="flex gap-1">
            <span className="h-2 w-2 rounded-full bg-white animate-bounce [animation-delay:-0.3s]" />
            <span className="h-2 w-2 rounded-full bg-white animate-bounce [animation-delay:-0.15s]" />
            <span className="h-2 w-2 rounded-full bg-white animate-bounce" />
          </span>
          <span>Pondering...</span>
        </span>
      ) : (
        children
      )}
    </button>
  );
}
