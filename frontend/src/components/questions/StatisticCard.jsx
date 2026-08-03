export default function StatisticCard({ title, children, isEmpty = false }) {
  return (
    <div className="statistic-card">
      <h3 className="statistic-card-title">{title}</h3>
      {isEmpty ? (
        <div className="statistic-empty">No data available yet.</div>
      ) : (
        <div className="statistic-card-body">{children}</div>
      )}
    </div>
  );
}
