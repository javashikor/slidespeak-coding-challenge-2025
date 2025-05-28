// Progress Indicator Component

interface ProgressIndicatorProps {
  text: string;
}

// Progress Indicator Component
export const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({ text }) => {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <div className="flex items-center space-x-3">
        <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <span className="text-gray-700 font-medium">{text}</span>
      </div>
    </div>
  );
};
