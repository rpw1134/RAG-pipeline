"use client";

import { useRef } from "react";

interface FileUploadProps {
  selectedFile: File | null;
  onFileSelect: (file: File) => void;
  accept?: string;
  compact?: boolean;
  required?: boolean;
}

export function FileUpload({
  selectedFile,
  onFileSelect,
  accept = ".pdf",
  compact = false,
  required = false,
}: FileUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onFileSelect(file);
  };

  const handleFileDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file) onFileSelect(file);
  };

  return (
    <div>
      <label className="mb-2 block text-sm font-medium">
        Document File{required && <span className="text-accent ml-1">*</span>}
      </label>
      <div
        onClick={() => fileInputRef.current?.click()}
        onDrop={handleFileDrop}
        onDragOver={(e) => e.preventDefault()}
        className={`flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-border bg-input-bg transition-colors hover:border-accent ${
          compact ? "px-4 py-4" : "px-6 py-8"
        }`}
      >
        {!compact && (
          <svg
            className="mb-3 h-10 w-10 text-muted"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        )}
        {selectedFile ? (
          <span className={`text-accent truncate max-w-full px-2 ${compact ? "text-xs" : "text-sm"}`}>
            {selectedFile.name}
          </span>
        ) : (
          <>
            <span className={`text-foreground ${compact ? "text-xs" : "text-sm"}`}>
              {compact ? "Click to upload" : "Click to upload or drag and drop"}
            </span>
            {!compact && (
              <span className="mt-1 text-xs text-muted">
                PDF only
              </span>
            )}
          </>
        )}
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileSelect}
          accept={accept}
          className="hidden"
        />
      </div>
    </div>
  );
}
