import { Card, CardContent, CardMedia, Typography } from "@mui/material";
import { Song } from "../schema/recommender.ts";

interface SongProps {
  song: Song;
  defaultImage?: string;
}

export function Recommendation({ song, defaultImage }: SongProps) {
  const image =
    defaultImage == undefined
      ? "https://www.pngmart.com/files/8/Compact-Disk-PNG-HD-Photo.png"
      : defaultImage;
  return (
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
        image={song.image || image}
        alt={song.name}
      />
      <CardContent>
        <Typography variant="subtitle1">{song.name}</Typography>
      </CardContent>
    </Card>
  );
}
