import { Button, SuccessCard } from "../ui";

export interface ConversionDoneProps {
  downloadUrl: string;
  onConvertAnother: () => void;
}

export const ConversionDone = ({
  downloadUrl,
  onConvertAnother,
}: ConversionDoneProps) => {
  return (
    <div className="max-w-md mx-auto rounded-2xl shadow-lg p-6 space-y-4">
      <SuccessCard />
      <div className="flex space-x-3">
        <Button
          onClick={onConvertAnother}
          variant="secondary"
          className="flex-1"
        >
          Convert another
        </Button>
        <a href={downloadUrl} download>
          <Button className="flex-1 flex items-center justify-center space-x-2">
            <span>Download file</span>
          </Button>
        </a>
      </div>
    </div>
  );
};