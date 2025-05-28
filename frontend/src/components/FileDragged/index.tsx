"use client";

import { useState } from "react";
import { Button, ConversionOption, FileInfoCard } from "../ui";

export const FileDragged = () => {
  const [selectedOption, setSelectedOption] = useState<string>("pdf");

  return (
    <div className="max-w-md mx-auto rounded-2xl shadow-lg p-6 space-y-4">
      <FileInfoCard
        fileName="Digital Marketing requirements.pptx"
        fileSize="3.88 MB"
      />
      <ConversionOption
        title="High Compression"
        description="Smallest file size, standard quality"
        selected={selectedOption === "pdf"}
        onClick={() => setSelectedOption("pdf")}
      />
      <div className="flex space-x-3">
        <Button variant="secondary" className="flex-1">
          Cancel
        </Button>
        <Button className="flex-1">Compress</Button>
      </div>
    </div>
  );
};
