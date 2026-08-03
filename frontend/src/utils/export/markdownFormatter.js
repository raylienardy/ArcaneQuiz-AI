function escapeMarkdown(text) {
  return text.replace(/_/g, "\\_").replace(/\*/g, "\\*");
}

export function formatMarkdown(questions) {
  let markdown = "";
  questions.forEach((q, idx) => {
    markdown += `## Pertanyaan ${idx + 1}\n\n`;
    markdown += `${q.question}\n\n`;

    if (q.type === "multiple_choice" && q.choices) {
      q.choices.forEach((choice) => {
        const marker = choice.label === q.answer ? "**" : "";
        markdown += `${marker}${choice.label}. ${escapeMarkdown(choice.text)}${marker}\n`;
      });
      markdown += "\n";
    } else if (q.type === "true_false") {
      markdown += `True / False?\n\n`;
    }

    if (q.answer) {
      markdown += `**Jawaban:** ${q.answer}\n\n`;
    }
    if (q.explanation) {
      markdown += `**Penjelasan:** ${q.explanation}\n\n`;
    }
    markdown += "---\n\n";
  });
  return markdown;
}
