export default function LoadingSkeleton({ lines = 4 }) {
  return (
    <div className="loading-skeleton">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="skeleton-line"
          style={{ width: `${Math.max(40, 100 - i * 10)}%` }}
        ></div>
      ))}
    </div>
  );
}
