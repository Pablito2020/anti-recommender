export interface Result<T> {
  isError: boolean;
  value?: T;
  error?: string;
}
