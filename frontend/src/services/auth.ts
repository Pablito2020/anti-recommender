import axios, { AxiosResponse } from "axios";
import { userIsLoggedIn } from "./recommender.ts";
import { Result } from "../schema/result.ts";
import { isApiError } from "../schema/error.ts";

const CURRENT_USER_KEY = "CurrentUser";

const parseAxiosResponse: (
  response: AxiosResponse,
  mail: string,
) => Result<null> = (_, mail) => {
  localStorage.setItem(CURRENT_USER_KEY, mail);
  return { isError: false, value: null };
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
  } catch (response: unknown) {
    if (axios.isAxiosError(response)) {
      const body = response.response;
      if (response.status == 400 && isApiError(body?.data))
        return {
          isError: true,
          error: `You messed it up with input data. Server says: \n ${body?.data.detail}`,
        };
      if (response.status == 409 && isApiError(body?.data))
        return {
          isError: true,
          error: `Wow, our backend is probably in a broken status (db in inconsistent state). The server says: \n ${body?.data.detail}`,
        };
      if (response.status == 502 && isApiError(body?.data))
        return {
          isError: true,
          error: `One of our "reverse-engineering-hacks" isn't working right now. Server says: \n ${body?.data.detail}`,
        };
      return {
        isError: true,
        error: `We don't really know what happened. Server says: \n ${body?.data?.detail}`,
      };
    }
    return {
      isError: true,
      error: `We don't know what went bad. It's not an axios error`,
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
