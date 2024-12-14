import { Box, Typography } from "@mui/material";
import { Recommendation } from "./recommendation.tsx";
import { Recommender } from "../schema/recommender.ts";

interface RandomRecommendationProps {
  data: Recommender;
}

export function RandomRecommendation({ data }: RandomRecommendationProps) {
  return (
    <>
      <Box sx={{ padding: 3, margin: "auto" }}>
        <Typography variant="h3" sx={{ marginTop: 4, padding: 2 }}>
          You're a real outsider! Your last songs don't appear on our dataset!
        </Typography>
        <Typography variant="h5" sx={{ marginTop: 4, padding: 2 }}>
          Anyway, we recommend you this random song:
        </Typography>
        <Recommendation song={data.recommended} />
      </Box>
    </>
  );
}
