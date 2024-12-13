import { useState } from "react";
import "./App.css";
import { Box, Button, Typography } from "@mui/material";
import AntiRecommender from "/antirecommender.svg";
import Login from "./components/login.tsx";

function App() {
  const [isInfering, setInfering] = useState<boolean>(false);
  const onBack = () => {
    setInfering(false);
  };
  const goInfer = () => {
    setInfering(true);
  };
  if (isInfering) {
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
        <Login onBack={onBack} />
      </Box>
    );
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
      <Button
        variant="contained"
        color="primary"
        size="large"
        onClick={goInfer}
      >
        Start!
      </Button>
    </Box>
  );
}

export default App;
