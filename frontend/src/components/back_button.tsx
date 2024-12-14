import { Button } from "@mui/material";

interface BackProps {
  onBack: () => void;
}

export function BackButton({ onBack }: BackProps) {
  return (
    <>
      <Button onClick={onBack}>Go Back!</Button>
    </>
  );
}
