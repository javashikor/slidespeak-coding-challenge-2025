// Shared Button Component

interface ButtonProps {
  variant?: "primary" | "secondary";
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}

export const Button = ({
  variant = "primary",
  children,
  onClick,
  disabled = false,
  className = "",
  
}: ButtonProps) => {
  const baseClasses = "px-6 py-3 rounded-lg font-medium transition-colors";
  const variants = {
    primary: "bg-blue-500 text-white text-sm",
    secondary: "bg-white text-gray-800 border border-gray-300 text-sm",
  };

  return (
    <button
      className={`${baseClasses} ${variants[variant]} ${disabled ? "opacity-50 cursor-not-allowed" : ""} ${className}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
