import { useState, useEffect } from "react";
import { SpotifyApi } from "@spotify/web-api-ts-sdk";
import { Scopes } from "./Scopes";
import axios from "axios";
import "./App.css";

function App() {
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any | null>(null);
  const spotifyClientId = "f3d641d567484158967a7832a6b8d418";
  const frontend = "http://localhost:5173";
  const backend = "http://localhost:8000";

  useEffect(() => {
    SpotifyApi.performUserAuthorization(
      spotifyClientId,
      frontend,
      Scopes.userRecents,
      async (userToken) => {
        try {
          const result = await axios.post(`${backend}/recommend`, userToken);
          setData(JSON.stringify(result.data));
        } catch (error: any) {
          setError(
            `Couldn't get information from your spotify account..${error.response.data.detail}`,
          );
        }
      },
    );
  }, []);

  if (error) {
    return <>An error happened! {error}</>;
  }
  if (data) {
    return <>We have data! {data}</>;
  }
  return <>You should login...</>;
}

export default App;
