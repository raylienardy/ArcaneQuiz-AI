import ErrorState from "./ErrorState";
import { mapApiError } from "../../utils/errorMapper";

export default function RetryCard({ error, onRetry }) {
  const { title, description, retry } = mapApiError(error);
  return (
    <ErrorState
      title={title}
      description={description}
      onRetry={retry ? onRetry : null}
    />
  );
}
