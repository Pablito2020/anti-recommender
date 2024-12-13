import axios, { AxiosResponse } from "axios";
import { Result } from "../schema/recommender.ts";

const parseAxiosResponse: (response: AxiosResponse) => Result<null> = (
  response,
) => {
  if (response.status == 200) {
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
    return parseAxiosResponse(response);
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
