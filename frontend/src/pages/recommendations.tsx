import { useEffect, useState } from "react";
import { getRecommendations } from "../services/recommender.ts";
import { Typography, Box } from "@mui/material";
import { Recommender } from "../schema/recommender.ts";
import { ErrorScreen } from "../components/error.tsx";
import { BackButton } from "../components/back_button.tsx";
import { Loading } from "../components/loading.tsx";
import { SongList } from "../components/song_list.tsx";
import { Recommendation } from "../components/recommendation.tsx";

interface SpotifyRecommenderProps {
  onBack: () => void;
}

function SpotifyRecommendations({ onBack }: SpotifyRecommenderProps) {
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<Recommender | null>(null);

  useEffect(() => {
    const fetchRecommendations = async () => {
      const recommendations = await getRecommendations();
      if (recommendations == null) {
        console.log("Recommendations is null. Probably spotify is loading....");
      } else if (recommendations.isError) {
        setError(recommendations.error!);
      } else {
        setData(recommendations.value!);
      }
    };
    fetchRecommendations();
  }, []);

  if (error) {
    return (
      <>
        <ErrorScreen onBack={onBack} error={error} />
      </>
    );
  }
  if (data) {
    return (
      <>
        <Box sx={{ padding: 3, maxWidth: 600, margin: "auto" }}>
          <Typography variant="h5" gutterBottom>
            From the following songs you listened:
          </Typography>
          <SongList songs={data.fromSongs} />

          <Typography variant="h6" sx={{ marginTop: 4 }}>
            Our Recommendation:
          </Typography>
          <Recommendation song={data.recommended} />
        </Box>
        <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
          <BackButton onBack={onBack} />
        </Box>
      </>
    );
  }
  return (
    <Loading
      message={
        "We're analyzing your song history and sending it to our model. Please wait"
      }
    />
  );
}

export default SpotifyRecommendations;
