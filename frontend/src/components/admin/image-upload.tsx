'use client';

import { useState, useRef } from 'react';

interface ImageUploadProps {
  label: string;
  currentImage: string | null;
  onChange: (file: File) => void;
  onRemove?: () => void;
}

export default function ImageUpload({ label, currentImage, onChange, onRemove }: ImageUploadProps) {
  const [preview, setPreview] = useState<string | null>(currentImage);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const objectUrl = URL.createObjectURL(file);
      setPreview(objectUrl);
      onChange(file);
    }
  };

  const handleRemove = () => {
    setPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    if (onRemove) onRemove();
  };

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-gray-300">{label}</label>
      <div className="relative group">
        {preview ? (
          <div className="relative w-full h-48 rounded-xl overflow-hidden border border-white/10 bg-white/5">
            <img src={preview} alt="Preview" className="w-full h-full object-fill" />
            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white backdrop-blur-sm transition-colors"
              >
                Change
              </button>
              {onRemove && (
                <button
                  type="button"
                  onClick={handleRemove}
                  className="p-2 bg-red-500/80 hover:bg-red-600/80 rounded-lg text-white backdrop-blur-sm transition-colors"
                >
                  Remove
                </button>
              )}
            </div>
          </div>
        ) : (
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="w-full h-48 rounded-xl border-2 border-dashed border-white/10 hover:border-purple-500/50 hover:bg-purple-500/5 bg-white/5 flex flex-col items-center justify-center text-gray-400 hover:text-purple-400 transition-all"
          >
            <svg className="w-8 h-8 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span className="text-sm font-medium">Click to upload image</span>
          </button>
        )}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="hidden"
        />
      </div>
    </div>
  );
}
