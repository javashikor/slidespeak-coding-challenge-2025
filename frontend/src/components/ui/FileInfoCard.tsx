// File Info Card Component

interface FileInfoCardProps {
  fileName: string;
  fileSize: string;
  className?: string;
}

export const FileInfoCard = ({
  fileName,
  fileSize,
  className = "",
}: FileInfoCardProps) => {
  return (
    <div
      className={`bg-white rounded-xl border border-gray-200 p-6 text-center ${className}`}
    >
      <h3 className="text-lg font-semibold text-gray-800 mb-2">{fileName}</h3>
      <p className="text-gray-500">{fileSize}</p>
    </div>
  );
};
