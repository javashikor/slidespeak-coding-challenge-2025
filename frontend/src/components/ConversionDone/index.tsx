import { Button, SuccessCard } from "../ui";

interface ConversionOptionProps {
  title: string;
  description: string;
  selected?: boolean;
  onClick?: () => void;
}

export const ConversionDone = () => {
  return (
    <div className="max-w-md mx-auto rounded-2xl shadow-lg p-6 space-y-4">
      <SuccessCard />
      <div className="flex space-x-3">
        <Button variant="secondary" className="flex-1">
          Convert another
        </Button>
        <Button className="flex-1 flex items-center justify-center space-x-2">
          <span>Download file</span>
        </Button>
      </div>
    </div>
  );
};
