export default function StatisticItem({ label, value }) {
  return (
    <div className="statistic-item">
      <span className="statistic-value">{value}</span>
      <span className="statistic-label">{label}</span>
    </div>
  );
}
