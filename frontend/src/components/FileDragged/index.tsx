"use client";

import { useState } from "react";
import { Button, ConversionOption, FileInfoCard } from "../ui";

export interface FileDraggedProps {
  fileName: string;
  fileSize: string;
  onRemove: () => void;
  onConvert: () => void;
  error?: string | null;
}

export const FileDragged = ({
  fileName,
  fileSize,
  onRemove,
  onConvert,
  error,
}: FileDraggedProps) => {
  const [selectedOption, setSelectedOption] = useState<string>("pdf");

  return !error ? (
    <div className="max-w-md mx-auto rounded-2xl shadow-lg p-6 space-y-4">
      <FileInfoCard fileName={fileName} fileSize={fileSize} />
      <ConversionOption
        title="High Compression"
        description="Smallest file size, standard quality"
        selected={selectedOption === "pdf"}
        onClick={() => setSelectedOption("pdf")}
      />
      <div className="flex space-x-3">
        <Button onClick={onRemove} variant="secondary" className="flex-1">
          Cancel
        </Button>
        <Button onClick={onConvert} className="flex-1">
          Compress
        </Button>
      </div>
    </div>
  ) : (
    <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
      <p className="text-red-700 text-sm">{error}</p>
    </div>
  );
};
