import React, { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  TextField,
  Typography,
} from "@mui/material";
import { addAccountToProject } from "../services/account.ts";
import CircularProgress from "@mui/material/CircularProgress";
import Recommendations from "./recommendations.tsx";

interface LoginProps {
  onBack: () => void;
}

function Login({ onBack }: LoginProps) {
  const [email, setEmail] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [nextScreen, setNextScreen] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  const sendMail = () => {
    const postMail = async () => {
      setLoading(true);
      const result = await addAccountToProject(email);
      setLoading(false);
      if (result.isError) {
        setError(result.error!);
      } else {
        setNextScreen(true);
      }
    };
    postMail();
  };

  const GoBackButton = () => {
    return (
      <>
        <Button onClick={onBack}>Go Back!</Button>
      </>
    );
  };

  if (error) {
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
              <GoBackButton />
            </Box>
          </CardContent>
        </Card>
      </Box>
    );
  }
  if (loading) {
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
          We're adding to our project database. Please wait....
        </Typography>
      </Box>
    );
  }

  if (nextScreen) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100%",
          width: "100%",
        }}
      >
        <Recommendations onBack={onBack} />
      </Box>
    );
  }

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        textAlign: "center",
      }}
    >
      <Typography variant="h5" gutterBottom>
        Add your Spotify mail here!
      </Typography>
      <TextField
        label="Email"
        variant="outlined"
        value={email}
        onChange={handleEmailChange}
        fullWidth
        sx={{ mb: 2 }} // margin bottom for spacing
      />
      <Button
        variant="contained"
        color="primary"
        size="large"
        onClick={sendMail}
      >
        Log In with Spotify!
      </Button>
    </Box>
  );
}

export default Login;
