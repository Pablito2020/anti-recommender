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
  recommendation: unknown,
): recommendation is Recommender =>
  typeof recommendation === "object" &&
  recommendation !== null &&
  Object.hasOwn(recommendation, "isRandom") &&
  // @ts-expect-error: We're sure it exists
  typeof recommendation.isRandom === "boolean";

export const isApiError = (error: unknown): error is ApiError =>
  typeof error === "object" &&
  error !== null &&
  Object.hasOwn(error, "detail") &&
  // @ts-expect-error: We're sure it exists
  typeof error.detail === "string";

export type RecommenderResult = Result<Recommender>;
