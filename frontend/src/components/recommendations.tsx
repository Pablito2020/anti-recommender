import { useEffect, useState } from "react";
import { getRecommendations } from "../services/recommender.ts";
import CircularProgress from "@mui/material/CircularProgress";
import { Button } from "@mui/material";
import { Recommender } from "../schema/recommender.ts";

interface SpotifyRecommenderProps {
  onBack: () => void;
}

function SpotifyRecommendations({ onBack }: SpotifyRecommenderProps) {
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<Recommender | null>(null);

  useEffect(() => {
    const fetchRecommendations = async () => {
      const recommendations = await getRecommendations();
      if (recommendations.isError) {
        setError(recommendations.error!);
      } else {
        setData(recommendations.value!);
      }
    };
    fetchRecommendations();
  }, []);

  const GoBackButton = () => {
    return (
      <>
        <Button onClick={onBack}>Go Back!</Button>
      </>
    );
  };

  if (error) {
    return (
      <>
        An error happened! {error}
        <GoBackButton />
      </>
    );
  }
  if (data) {
    return (
      <>
        We have data! {JSON.stringify(data)}
        <GoBackButton />
      </>
    );
  }
  return (
    <>
      <CircularProgress color="secondary" />
    </>
  );
}

export default SpotifyRecommendations;
