import StatisticItem from "./StatisticItem";

export default function StatisticGroup({ title, items }) {
  if (!items || items.length === 0) return null;
  return (
    <div className="statistic-group">
      <h4 className="statistic-group-title">{title}</h4>
      <div className="statistic-group-items">
        {items.map((item, idx) => (
          <StatisticItem key={idx} label={item.label} value={item.value} />
        ))}
      </div>
    </div>
  );
}
