import { useCallback, useEffect, useRef, useState } from "react";

interface JobStatus {
  status: string;
  progress: number;
  message: string;
  stage: string;
  download_url?: string;
}

type ConversionState =
  | "idle"
  | "uploading"
  | "converting"
  | "success"
  | "error";

interface ConversionResult {
  success: boolean;
  message: string;
  job_id: string;
  download_url?: string;
}

export const useFileConverter = () => {
  const [file, setFile] = useState<File | null>(null);
  const [conversionState, setConversionState] =
    useState<ConversionState>("idle");
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const pollJobStatus = useCallback(async (jobId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/status/${jobId}`);
      if (response.ok) {
        const status: JobStatus = await response.json();
        setJobStatus(status);

        if (status.status === "complete" || status.status === "error") {
          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
          }

          setConversionState(
            status.status === "complete" ? "success" : "error"
          );

          if (status.status === "error") {
            setError(status.message);
          }
        }
      }
    } catch (err) {
      console.error("Error polling job status:", err);
      setError("Failed to check conversion status");
      setConversionState("error");
    }
  }, []);

  const startConversion = useCallback(
    async (selectedFile: File) => {
      if (!selectedFile.name.endsWith(".pptx")) {
        setError("Please select a PPTX file");
        return;
      }

      setConversionState("converting");
      setError(null);
      setJobStatus(null);

      try {
        const formData = new FormData();
        formData.append("file", selectedFile);

        const response = await fetch(
          "http://localhost:8000/convert/pptx-to-pdf",
          {
            method: "POST",
            body: formData,
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Conversion failed");
        }

        const result: ConversionResult = await response.json();

        if (result.success) {
          if (result.download_url) {
            setJobStatus({
              status: "complete",
              progress: 100,
              message: result.message,
              stage: "complete",
              download_url: result.download_url,
            });
            setConversionState("success");
          } else if (result.job_id) {
            pollIntervalRef.current = setInterval(() => {
              pollJobStatus(result.job_id);
            }, 1000);
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
        setConversionState("error");
      }
    },
    [pollJobStatus]
  );

  const resetConverter = useCallback(() => {
    setFile(null);
    setConversionState("idle");
    setJobStatus(null);
    setError(null);
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
  }, []);

  const selectFile = useCallback((selectedFile: File) => {
    setFile(selectedFile);
    setError(null);
    setJobStatus(null);
    setConversionState("idle");
  }, []);

  useEffect(() => {
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  return {
    file,
    conversionState,
    jobStatus,
    error,
    selectFile,
    startConversion,
    resetConverter,
  };
};
