import { useEffect, useState } from "react";
import { getRecommendations } from "../services/recommender.ts";
import CircularProgress from "@mui/material/CircularProgress";
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Box,
  Button,
} from "@mui/material";
import { Recommender } from "../schema/recommender.ts";
import vite from "/vite.svg";

interface SpotifyRecommenderProps {
  onBack: () => void;
}

const defaultImage = vite;

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
  if (data) {
    return (
      <>
        <Box sx={{ padding: 3, maxWidth: 600, margin: "auto" }}>
          <Typography variant="h5" gutterBottom>
            From the following songs you listened:
          </Typography>

          <Box
            sx={{
              display: "flex",
              gap: 2,
              flexWrap: "wrap",
              justifyContent: "center",
            }}
          >
            {data.fromSongs.map((song, index) => (
              <Card
                key={index}
                sx={{
                  flex: "1 1 calc(25% - 16px)",
                  maxWidth: 150,
                  minWidth: 100,
                }}
              >
                <CardMedia
                  component="img"
                  height="150"
                  image={song.image || defaultImage}
                  alt={song.name}
                />
                <CardContent>
                  <Typography variant="subtitle1" noWrap>
                    {song.name}
                  </Typography>
                </CardContent>
              </Card>
            ))}
          </Box>

          <Typography variant="h6" sx={{ marginTop: 4 }}>
            Our Recommendation:
          </Typography>
          <Card
            sx={{
              display: "flex",
              alignItems: "center",
              maxWidth: "100%",
              margin: "auto",
              flexWrap: "wrap",
              gap: 1,
            }}
          >
            <CardMedia
              component="img"
              sx={{
                width: { xs: 80, sm: 100 },
                height: { xs: 80, sm: 100 },
              }}
              image={data.recommended.image || defaultImage}
              alt={data.recommended.name}
            />
            <CardContent>
              <Typography variant="subtitle1">
                {data.recommended.name}
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
          <GoBackButton />
        </Box>
      </>
    );
  }
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
        We're analyzing your song history and passing it to our model, please
        wait.
      </Typography>
    </Box>
  );
}

export default SpotifyRecommendations;
