import { Result } from "./result.ts";

export interface Song {
  id: string;
  name: string;
  image?: string;
}

export interface Recommender {
  isRandom: boolean;
  fromSongs: Song[];
  recommended: Song;
}

export const isRecommender = (
  recommendation: unknown,
): recommendation is Recommender =>
  typeof recommendation === "object" &&
  recommendation !== null &&
  Object.hasOwn(recommendation, "isRandom") &&
  // @ts-expect-error: We're sure it exists
  typeof recommendation.isRandom === "boolean";

export type RecommenderResult = Result<Recommender>;
