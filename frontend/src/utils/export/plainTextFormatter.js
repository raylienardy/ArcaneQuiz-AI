/**
 * Mengembalikan hanya teks pertanyaan (tanpa jawaban/penjelasan).
 */
export function formatQuestionsOnly(questions) {
  return questions
    .map((q, idx) => {
      let text = `${idx + 1}. ${q.question}`;
      if (q.choices && q.choices.length > 0) {
        text +=
          "\n" + q.choices.map((c) => `   ${c.label}. ${c.text}`).join("\n");
      }
      return text;
    })
    .join("\n\n");
}
