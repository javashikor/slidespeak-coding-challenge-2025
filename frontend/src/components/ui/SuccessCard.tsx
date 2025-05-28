// Success Card Component

import { CheckIcon } from "@/icons/CheckIcon";
import UploadIcon from "@/icons/UploadIcon";

interface SuccessCardProps {
  className?: string;
}
export const SuccessCard = ({ className = "" }: SuccessCardProps) => {
  return (
    <div
      className={`bg-white rounded-xl border border-gray-200 p-8 text-center ${className}`}
    >
      <div className="flex justify-center mb-4">
        <div className="relative">
          <UploadIcon />
          <div className="absolute -bottom-1 -right-1 bg-green-500 rounded-full p-1">
            <CheckIcon />
          </div>
        </div>
      </div>
      <h3 className="text-lg font-semibold text-gray-800">
        File converted successfully!
      </h3>
    </div>
  );
};
