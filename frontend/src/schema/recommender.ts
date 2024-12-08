export interface Result<T> {
  isError: boolean;
  value?: T;
  error?: string;
}

export interface Song {
  name: string;
  image?: string;
}

export interface Recommender {
  isRandom: boolean;
  fromSongs: Song[];
  recommended: Song;
}

export interface ApiError {
  detail: string;
}

export const isRecommender = (
  recommendation: any,
): recommendation is Recommender =>
  typeof recommendation === "object" &&
  recommendation !== null &&
  recommendation.hasOwnProperty("isRandom") &&
  typeof recommendation.isRandom === "boolean";

export const isApiError = (error: any): error is ApiError =>
  typeof error === "object" &&
  error !== null &&
  error.hasOwnProperty("detail") &&
  typeof error.detail === "string";

export type RecommenderResult = Result<Recommender>;
