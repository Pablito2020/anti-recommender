import { Box, Card, CardContent, Typography } from "@mui/material";
import { BackButton } from "./back_button.tsx";

interface ErrorProps {
  onBack: () => void;
  error: string;
}

export function ErrorScreen({ onBack, error }: ErrorProps) {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        padding: 2,
        backgroundColor: "#f8d7da",
      }}
    >
      <Card
        sx={{
          backgroundColor: "#f44336",
          color: "#fff",
          width: "100%",
          maxWidth: 400,
          padding: 2,
        }}
      >
        <CardContent>
          <Typography variant="h6" align="center" gutterBottom>
            An error happened!
          </Typography>
          <Typography variant="body1" align="center">
            {error}
          </Typography>
          <Box sx={{ mt: 2, display: "flex", justifyContent: "center" }}>
            <BackButton onBack={onBack} />
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}
