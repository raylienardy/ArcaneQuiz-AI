import { useMemo } from "react";
import { calculateQuestionStatistics } from "../../utils/questionStatistics";
import StatisticCard from "./StatisticCard";
import StatisticGroup from "./StatisticGroup";

export default function QuestionAnalyticsPanel({ questions, provider, model }) {
  const stats = useMemo(() => {
    const base = calculateQuestionStatistics(questions);
    // Tambahkan info provider jika tersedia
    base.provider = provider || null;
    return base;
  }, [questions, provider]);

  // Siapkan item untuk Question Types
  const typeItems = Object.entries(stats.question_types).map(
    ([type, count]) => ({
      label: type.replace("_", " "),
      value: count,
    }),
  );

  // Difficulty items (jika ada)
  const difficultyItems = Object.entries(stats.difficulty).map(
    ([level, count]) => ({
      label: level,
      value: count,
    }),
  );

  // Language items (jika ada)
  const languageItems = Object.entries(stats.language).map(([lang, count]) => ({
    label: lang,
    value: count,
  }));

  // Provider info
  const providerDisplay = stats.provider
    ? `${stats.provider}${model ? ` (${model})` : ""}`
    : "Unknown";

  return (
    <div className="question-analytics-panel">
      <h2 className="analytics-title">Question Analytics</h2>
      <div className="analytics-cards">
        <StatisticCard title="Total Questions">
          <div className="total-questions-value">{stats.total_questions}</div>
        </StatisticCard>

        <StatisticCard title="Question Types" isEmpty={typeItems.length === 0}>
          <StatisticGroup items={typeItems} />
        </StatisticCard>

        <StatisticCard
          title="Difficulty"
          isEmpty={difficultyItems.length === 0}
        >
          {difficultyItems.length > 0 ? (
            <StatisticGroup items={difficultyItems} />
          ) : (
            <div className="coming-soon">Coming Soon</div>
          )}
        </StatisticCard>

        <StatisticCard title="Language" isEmpty={languageItems.length === 0}>
          {languageItems.length > 0 ? (
            <StatisticGroup items={languageItems} />
          ) : (
            <div className="coming-soon">Coming Soon</div>
          )}
        </StatisticCard>

        <StatisticCard title="Provider">
          <div className="provider-info">{providerDisplay}</div>
        </StatisticCard>
      </div>
    </div>
  );
}
