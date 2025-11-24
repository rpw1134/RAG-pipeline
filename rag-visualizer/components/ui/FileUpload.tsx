"use client";

import { useRef } from "react";

interface FileUploadProps {
  selectedFile: File | null;
  onFileSelect: (file: File) => void;
  accept?: string;
}

export function FileUpload({
  selectedFile,
  onFileSelect,
  accept = ".pdf,.txt,.md,.docx",
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
      <label className="mb-2 block text-sm font-medium">Document File</label>
      <div
        onClick={() => fileInputRef.current?.click()}
        onDrop={handleFileDrop}
        onDragOver={(e) => e.preventDefault()}
        className="flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-border bg-input-bg px-6 py-8 transition-colors hover:border-accent"
      >
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
        {selectedFile ? (
          <span className="text-sm text-accent">{selectedFile.name}</span>
        ) : (
          <>
            <span className="text-sm text-foreground">
              Click to upload or drag and drop
            </span>
            <span className="mt-1 text-xs text-muted">
              PDF, TXT, MD, or DOCX
            </span>
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
