import { Box, Card, CardContent, CardMedia, Typography } from "@mui/material";
import { Song } from "../schema/recommender";

interface SongListProps {
  songs: Song[];
  defaultImage?: string;
}

export function SongList({ songs, defaultImage }: SongListProps) {
  const image =
    defaultImage == undefined
      ? "https://www.pngmart.com/files/8/Compact-Disk-PNG-HD-Photo.png"
      : defaultImage;
  return (
    <Box
      sx={{
        display: "flex",
        gap: 2,
        flexWrap: "wrap",
        justifyContent: "center",
      }}
    >
      {songs.map((song, index) => (
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
            image={song.image || image}
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
  );
}
