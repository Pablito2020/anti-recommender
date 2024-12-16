export interface ApiError {
  detail: string;
}

export const isApiError = (error: unknown): error is ApiError =>
  typeof error === "object" &&
  error !== null &&
  Object.hasOwn(error, "detail") &&
  // @ts-expect-error: We're sure it exists
  typeof error.detail === "string";
