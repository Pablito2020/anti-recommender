import { useEffect, useState } from "react";
import "./App.css";
import Recommendations from "./components/recommendations.tsx";
import { Box, Button, Typography } from "@mui/material";
import AntiRecommender from "/antirecommender.svg";
import { userIsLoggedIn } from "./services/recommender.ts";

function App() {
  const [isInfering, setInfering] = useState<boolean>(false);
  const [isLoggedIn, setLogin] = useState<boolean>(false);
  const onBack = () => {
    setInfering(false);
  };
  const goInfer = () => {
    setInfering(true);
  };
  useEffect(() => {
    const setLoggedInInfo = async () => {
      const logged = await userIsLoggedIn();
      setLogin(logged);
    };
    setLoggedInInfo();
  }, []);

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
        <Recommendations onBack={onBack} />
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
  const buttonText = isLoggedIn ? "Start!" : "Log In";
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
        {buttonText}
      </Button>
    </Box>
  );
}

export default App;
