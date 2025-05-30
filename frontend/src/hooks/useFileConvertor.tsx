import { useCallback, useEffect, useRef, useState } from "react";

interface JobStatus {
  status: string;
  progress?: number;
  message: string;
  s3_url?: string;
  error?: string;
  job_id?: string;
}

type ConversionState =
  | "pending"
  | "started"
  | "in_progress"
  | "completed"
  | "error"
  | "unknown";

interface ConversionResult {
  success: boolean;
  message: string;
  job_id: string;
  status: string;
  download_url?: string;
}

export const useFileConverter = () => {
  const [file, setFile] = useState<File | null>(null);
  const [conversionState, setConversionState] =
    useState<ConversionState>("unknown");
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const pollJobStatus = useCallback(async (jobId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/status/${jobId}`);
      if (response.ok) {
        const status: JobStatus = await response.json();

        // // Debug logging
        // console.log("Polling status:", status);

        // Update job status
        setJobStatus(status);

        // Map backend status to frontend state
        const newState = status.status;
        // console.log("Mapped state:", newState);
        setConversionState(newState as ConversionState);

        // Handle completion or error - check for both "completed" and "SUCCESS" (Celery state)
        const isCompleted =
          status.status === "completed" || status.status === "SUCCESS";
        const isError =
          status.status === "error" || status.status === "FAILURE";

        if (isCompleted || isError) {
          // console.log("Job finished:", {
          //   isCompleted,
          //   isError,
          //   status: status.status,
          // });

          if (pollIntervalRef.current) {
            clearInterval(pollIntervalRef.current);
            pollIntervalRef.current = null;
          }

          if (isError) {
            setError(status.error || status.message || "Conversion failed");
            setConversionState("error");
          } else if (isCompleted) {
            setConversionState("completed");
          }
        }
      } else {
        // console.error("Failed to fetch job status");
        setError("Failed to fetch job status");
        setConversionState("error");
        if (pollIntervalRef.current) {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = null;
        }
      }
    } catch (err) {
      // console.error("Failed to check conversion status:", err);
      setError("Failed to check conversion status");
      setConversionState("error");
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    }
  }, []);

  const startConversion = useCallback(
    async (selectedFile: File) => {
      if (!selectedFile.name.endsWith(".pptx")) {
        setError("Please select a PPTX file");
        return;
      }

      setConversionState("pending");
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

        if (result.success && result.job_id) {
          // Set initial job status
          setJobStatus({
            status: result.status || "pending",
            message: result.message,
            job_id: result.job_id,
          });

          // Start polling every 2 seconds instead of 1
          pollIntervalRef.current = setInterval(() => {
            pollJobStatus(result.job_id);
          }, 2000);

          // Also poll once immediately
          pollJobStatus(result.job_id);
        } else {
          setError(result.message || "Conversion failed");
          setConversionState("error");
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
    setConversionState("unknown");
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
    setConversionState("unknown");
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
