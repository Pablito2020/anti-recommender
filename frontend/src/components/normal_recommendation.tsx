import { Box, Typography } from "@mui/material";
import { Recommendation } from "./recommendation.tsx";
import { SongList } from "./song_list.tsx";
import { Recommender } from "../schema/recommender.ts";

interface NormalRecommendationProps {
  data: Recommender;
}

export function NormalRecommendation({ data }: NormalRecommendationProps) {
  return (
    <>
      <Box sx={{ padding: 3, margin: "auto" }}>
        <Typography variant="h5" sx={{ marginTop: 4, padding: 2 }}>
          Our Recommendation:
        </Typography>
        <Recommendation song={data.recommended} />
        <Typography variant="h5" gutterBottom sx={{ padding: 2 }}>
          Because you listened the following songs:
        </Typography>
        <SongList songs={data.fromSongs} />
      </Box>
    </>
  );
}
