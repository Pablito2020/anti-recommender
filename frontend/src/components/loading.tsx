import { Box, Typography } from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";

interface LoadingProps {
  message: string;
}

export function Loading({ message }: LoadingProps) {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        textAlign: "center",
        padding: 2,
      }}
    >
      <CircularProgress color="secondary" />
      <Typography variant="h6" mt={2}>
        {message}
      </Typography>
    </Box>
  );
}
