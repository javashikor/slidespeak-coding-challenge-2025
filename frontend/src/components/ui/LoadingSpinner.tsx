// Loading Spinner Component

import { LoadingIndicatorIcon } from "@/icons/LoadingIndicatorIcon";

// Loading Spinner Component
export const LoadingSpinner: React.FC = () => {
  return (
    <div className="flex items-center justify-center animate-spin">
      <LoadingIndicatorIcon />
    </div>
  );
};
