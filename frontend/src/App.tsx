import { useState } from "react";
import "./App.css";
import Recommendations from "./components/recommendations.tsx";
import { Button } from "@mui/material";

function App() {
  const [isInfering, setInfering] = useState<boolean>(false);
  const onBack = () => {
    setInfering(false);
  };
  const goInfer = () => {
    setInfering(true);
  };

  if (isInfering) {
    return <Recommendations onBack={onBack} />;
  }
  return (
    <>
      Welcome to spotify anti recommender! Are you ready to be bad?
      <Button onClick={goInfer}>Yes!</Button>
    </>
  );
}

export default App;
