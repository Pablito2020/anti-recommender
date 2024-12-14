import { useState } from "react";
import "./App.css";
import { Box, Button, Typography } from "@mui/material";
import AntiRecommender from "/antirecommender.svg";
import Login from "./pages/login.tsx";
import {
  isAuthenticatedInProjectAndInSpotify,
  isUserAuthenticatedInProject,
  removeUserFromAuth,
} from "./services/auth.ts";
import Recommendations from "./pages/recommendations.tsx";

function App() {
  const [goNext, setGoNext] = useState<boolean>(false);
  const moveOn = () => {
    setGoNext(true);
  };
  const cleanData = () => {
    removeUserFromAuth();
  };

  if (isAuthenticatedInProjectAndInSpotify()) {
    return <Recommendations onBack={cleanData} />;
  }
  if (goNext && !isUserAuthenticatedInProject()) {
    return <Login onBack={cleanData} />;
  }
  const styles = {
    icon: {
      width: "100px",
      height: "100px", // Adjust the size as needed
      marginBottom: "20px",
    },
  };
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
      <img src={AntiRecommender} alt="App Icon" style={styles.icon} />
      <Typography variant="h5" gutterBottom>
        Welcome to Spotify Anti-Recommender! Are you ready to be bad?
      </Typography>
      <Button variant="contained" color="primary" size="large" onClick={moveOn}>
        Start!
      </Button>
    </Box>
  );
}

export default App;
