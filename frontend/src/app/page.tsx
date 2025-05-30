"use client";

import { ChooseFileStep } from "@/components/ChooseFileStep";
import { ConversionDone } from "@/components/ConversionDone";
import { ConversionInProgress } from "@/components/ConversionInProgress";
import { FileDragged } from "@/components/FileDragged";
import { useFileConverter } from "@/hooks/useFileConvertor";

const Home = () => {
  const {
    file,
    conversionState,
    jobStatus,
    error,
    selectFile,
    startConversion,
    resetConverter,
  } = useFileConverter();

  const handleConvert = () => {
    if (file) {
      startConversion(file);
    }
  };

  const formatFileSize = (bytes: number): string => {
    return (bytes / 1024 / 1024).toFixed(2) + " MB";
  };

  return (
    <main className="w-full h-screen flex items-center justify-center">
      <div className="w-full max-w-[420px]">
        {/* Error State */}
        {conversionState === "error" && (
          <div className="max-w-md mx-auto bg-gray-50 rounded-2xl shadow-lg p-6">
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700 text-sm">
                {error || "An error occurred during conversion"}
              </p>
            </div>
            <button
              onClick={resetConverter}
              className="mt-4 w-full bg-blue-500 hover:bg-blue-600 text-white font-medium px-6 py-3 rounded-lg transition-colors"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Converting States - pending, started, in_progress */}
        {(conversionState === "pending" ||
          conversionState === "started" ||
          conversionState === "in_progress") &&
          file && (
            <ConversionInProgress
              fileName={file.name}
              fileSize={formatFileSize(file.size)}
              progress={jobStatus?.progress}
              onCancel={resetConverter}
            />
          )}

        {/* Success State */}
        {conversionState === "completed" && jobStatus?.s3_url && (
          <ConversionDone
            downloadUrl={jobStatus.s3_url}
            onConvertAnother={resetConverter}
          />
        )}

        {/* File Selected State - show when file is selected but not converting */}
        {file && conversionState === "unknown" && !error && (
          <FileDragged
            fileName={file.name}
            fileSize={formatFileSize(file.size)}
            onRemove={resetConverter}
            onConvert={handleConvert}
            error={error}
          />
        )}

        {/* Initial Upload State - show when no file selected */}
        {!file && conversionState === "unknown" && (
          <ChooseFileStep
            onFileSelect={selectFile}
            error={error}
            disabled={false}
          />
        )}
      </div>
    </main>
  );
};

export default Home;
