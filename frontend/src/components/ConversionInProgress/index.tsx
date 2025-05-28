import { Button, FileInfoCard, ProgressIndicator } from "../ui";
import { LoadingSpinner } from "../ui/LoadingSpinner";

export const ConversionInProgress = () => {
  return (
    <div className="max-w-md mx-auto rounded-2xl shadow-lg p-6 space-y-4">
      <FileInfoCard
        fileName="Digital Marketing requirements.pptx"
        fileSize="5.5 MB"
      />
      <ProgressIndicator text="Converting your file" />
      <div className="flex space-x-3">
        <Button variant="secondary" className="flex-1" disabled>
          Cancel
        </Button>
        <Button className="flex-1" disabled>
          <LoadingSpinner />
        </Button>
      </div>
    </div>
  );
};
