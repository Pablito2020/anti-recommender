import axios, { AxiosResponse } from "axios";
import { Result } from "../schema/recommender.ts";
import { userIsLoggedIn } from "./recommender.ts";

const CURRENT_USER_KEY = "CurrentUser";

const parseAxiosResponse: (
  response: AxiosResponse,
  mail: string,
) => Result<null> = (response, mail) => {
  if (response.status == 200) {
    localStorage.setItem(CURRENT_USER_KEY, mail);
    return { isError: false, value: null };
  }
  return {
    isError: true,
    error: `You have something bad: ${response.data?.detail}`,
  };
};

const addAccount: (mail: string, url: string) => Promise<Result<null>> = async (
  mail,
  url,
) => {
  try {
    const response = await axios.post(`${url}/user`, {
      mail: mail,
    });
    return parseAxiosResponse(response, mail);
  } catch (error: unknown) {
    if (axios.isAxiosError(error))
      return {
        isError: true,
        error: `We couldn't contact the Backend API. Error: ${error.message}`,
      };
    return {
      isError: true,
      error: `We don't know what went bad. Sorry for that`,
    };
  }
};

export const addAccountToProject: (
  email: string,
) => Promise<Result<null>> = async (email) => {
  const backend = window.env.BACKEND_URL;
  if (!backend) {
    return {
      isError: true,
      error: "Person who deployed the app didn't specify spotify a backend url",
    };
  }
  return await addAccount(email, backend);
};

export function isUserAuthenticatedInProject(): boolean {
  return localStorage.getItem(CURRENT_USER_KEY) != null;
}

export function isAuthenticatedInProjectAndInSpotify(): boolean {
  return isUserAuthenticatedInProject() && userIsLoggedIn();
}

export function removeUserFromAuth() {
  if (isUserAuthenticatedInProject()) {
    localStorage.removeItem(CURRENT_USER_KEY);
  }
}
