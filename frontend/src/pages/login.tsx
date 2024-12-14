import React, { useState } from "react";
import { Box, Button, TextField, Typography } from "@mui/material";
import { addAccountToProject } from "../services/auth.ts";
import Recommendations from "./recommendations.tsx";
import { ErrorScreen } from "../components/error.tsx";
import { Loading } from "../components/loading.tsx";

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

  if (error) {
    return <ErrorScreen onBack={onBack} error={error} />;
  }
  if (loading) {
    return (
      <Loading
        message={
          "We're adding you to our allowed users database. Please wait...."
        }
      ></Loading>
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
