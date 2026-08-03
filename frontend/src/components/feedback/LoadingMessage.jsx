import LoadingSpinner from "./LoadingSpinner";
import { getLoadingMessage } from "../../utils/loadingMessages";

export default function LoadingMessage({ stage }) {
  const message = getLoadingMessage(stage);
  return (
    <div className="loading-message">
      <LoadingSpinner size={36} />
      <p>{message}</p>
    </div>
  );
}
