import { Scopes, SpotifyApi } from "@spotify/web-api-ts-sdk";
import axios, { AxiosResponse } from "axios";
import {
  isApiError,
  isRecommender,
  Recommender,
  RecommenderResult,
  Result,
} from "../schema/recommender.ts";

const SPOTIFY_TOKEN_LOCALSTORAGE = "spotify-sdk:verifier";
const SPOTIFY_TOKEN_PKCE =
  "spotify-sdk:AuthorizationCodeWithPKCEStrategy:token";

const parseAxiosResponse: (response: AxiosResponse) => Result<Recommender> = (
  response,
) => {
  const data = response.data;
  if (isRecommender(data)) {
    return {
      isError: false,
      value: data,
    };
  } else if (isApiError(data)) {
    return {
      isError: true,
      error: `The API says we did something bad :(. She says: ${data.detail}`,
    };
  } else {
    return {
      isError: true,
      error: `The API returned something that we didn't expect.`,
    };
  }
};

const getApiRecommendation: (
  userToken: unknown,
) => Promise<Result<Recommender>> = async (userToken) => {
  const backend = window.env.BACKEND_URL;
  if (!backend) {
    return {
      isError: true,
      error:
        "Person who deployed the app didn't specify a backend server url in frontend...",
    };
  }
  try {
    const response = await axios.post(`${backend}/recommend`, userToken);
    return parseAxiosResponse(response);
  } catch (error: unknown) {
    if (axios.isAxiosError(error))
      return {
        isError: true,
        error: `We couldn't contact the API. Error: ${error.message}`,
      };
    return {
      isError: true,
      error: `We don't know what went bad. Sorry for that`,
    };
  }
};

export const userIsLoggedIn: () => boolean = () => {
  const token = localStorage.getItem(SPOTIFY_TOKEN_LOCALSTORAGE);
  const pkce = localStorage.getItem(SPOTIFY_TOKEN_PKCE);
  return token != null || pkce != null;
};

export function deleteUserToken() {
  if (userIsLoggedIn()) {
    localStorage.removeItem(SPOTIFY_TOKEN_LOCALSTORAGE);
    localStorage.removeItem(SPOTIFY_TOKEN_PKCE);
  }
}

export const getRecommendations: () => Promise<Result<Recommender> | null> =
  async () => {
    const spotifyClientId = window.env.SPOTIFY_CLIENT_ID;
    const frontend = window.env.FRONTEND_URL;
    if (!spotifyClientId || !frontend) {
      return {
        isError: true,
        error:
          "Person who deployed the app didn't specify spotify a client id or frontend id",
      };
    }
    let result: RecommenderResult | null = null;
    await SpotifyApi.performUserAuthorization(
      spotifyClientId,
      frontend,
      Scopes.userRecents,
      async (userToken) => {
        result = await getApiRecommendation(userToken);
      },
    );
    return result;
  };
