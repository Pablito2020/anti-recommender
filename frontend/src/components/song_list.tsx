import { useState } from "react";
import {
  Box,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
} from "@mui/material";
import { Song } from "../schema/recommender";

interface SongListProps {
  songs: Song[];
  defaultImage?: string;
  maxHeight?: number;
  pageSize?: number;
}

const MAX_SONGS_PER_PAGE = 5;

export function SongList({
  songs,
  defaultImage,
  maxHeight = 400, // Default maxHeight
  pageSize = MAX_SONGS_PER_PAGE,
}: SongListProps) {
  const [currentPage, setCurrentPage] = useState(0);

  const image =
    defaultImage ??
    "https://www.pngmart.com/files/8/Compact-Disk-PNG-HD-Photo.png";

  // Calculate pagination
  const totalPages = Math.ceil(songs.length / pageSize);
  const paginatedSongs = songs.slice(
    currentPage * pageSize,
    (currentPage + 1) * pageSize,
  );

  const handleNextPage = () => {
    setCurrentPage((prev) => Math.min(prev + 1, totalPages - 1));
  };

  const handlePrevPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 0));
  };

  return (
    <Box
      sx={{
        maxHeight,
        overflowY: "auto",
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      <Box
        sx={{
          display: "flex",
          gap: 2,
          flexWrap: "wrap",
          justifyContent: "center",
        }}
      >
        {paginatedSongs.map((song, index) => (
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
      {/* Pagination controls */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          gap: 2,
          marginTop: 2,
        }}
      >
        <Button
          variant="contained"
          onClick={handlePrevPage}
          disabled={currentPage === 0}
        >
          Previous
        </Button>
        <Typography
          variant="body2"
          sx={{
            alignSelf: "center",
          }}
        >
          Your last {(currentPage + 1) * pageSize} songs of the{" "}
          {totalPages * pageSize} you listened
        </Typography>
        <Button
          variant="contained"
          onClick={handleNextPage}
          disabled={currentPage === totalPages - 1}
        >
          Next
        </Button>
      </Box>
    </Box>
  );
}
