import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import {createTheme} from "@mui/material/styles";
import {CssBaseline, ThemeProvider} from "@mui/material";

const THEME = createTheme({
    typography: {
        "fontFamily": `"Poppins", "Helvetica", "Arial", sans-serif`,
        "fontSize": 14,
        "fontWeightLight": 300,
        "fontWeightRegular": 400,
        "fontWeightMedium": 500
    },
    palette: {
        primary: {
            light: "#020202",
            main: "#1DB954",
            dark: "#79e8a0",
            contrastText: "#000000",
        },
        mode: "dark",
        background: {
            default: "#000000",
        },
        text: {
            primary: "#ffffff",
            secondary: "#000000",
        }
    }
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
      <ThemeProvider theme={THEME}>
          <CssBaseline />
          <App/>
      </ThemeProvider>
  </StrictMode>,
);
