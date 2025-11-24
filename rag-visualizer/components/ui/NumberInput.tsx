"use client";

import { useState, useEffect } from "react";

interface NumberInputProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
}

export function NumberInput({
  label,
  value,
  onChange,
  min = 1,
  max = 100,
}: NumberInputProps) {
  const [inputValue, setInputValue] = useState(String(value));

  useEffect(() => {
    setInputValue(String(value));
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setInputValue(val);

    const num = Number(val);
    if (val !== "" && !isNaN(num)) {
      onChange(num);
    }
  };

  const handleBlur = () => {
    if (inputValue === "" || isNaN(Number(inputValue))) {
      setInputValue(String(min));
      onChange(min);
    }
  };

  return (
    <div>
      <label className="mb-2 block text-sm font-medium">{label}</label>
      <input
        type="number"
        min={min}
        max={max}
        value={inputValue}
        onChange={handleChange}
        onBlur={handleBlur}
        className="w-full rounded-lg border border-border bg-input-bg px-4 py-2.5 text-sm focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent"
      />
    </div>
  );
}
