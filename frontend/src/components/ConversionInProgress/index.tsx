import { Button, FileInfoCard, ProgressIndicator } from "../ui";
import { LoadingSpinner } from "../ui/LoadingSpinner";

export interface ConversionInProgressProps {
  fileName: string;
  fileSize: string;
  progress?: number;
  onCancel: () => void;
}

export const ConversionInProgress = ({
  fileName,
  fileSize,
  progress,
  onCancel,
}: ConversionInProgressProps) => {
  return (
    <div className="max-w-md mx-auto rounded-2xl shadow-lg p-6 space-y-4">
      <FileInfoCard fileName={fileName} fileSize={fileSize} />
      <ProgressIndicator text="Converting your file" />
      <div className="flex space-x-3">
        <Button
          onClick={onCancel}
          variant="secondary"
          className="flex-1"
          disabled={progress !== undefined && progress < 100}
        >
          Cancel
        </Button>
        <Button
          className="flex-1"
          disabled={progress !== undefined && progress < 100}
        >
          <LoadingSpinner />
        </Button>
      </div>
    </div>
  );
};
