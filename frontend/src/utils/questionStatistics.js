/**
 * Menghitung statistik dari array pertanyaan.
 * @param {Array} questions - Array objek pertanyaan.
 * @returns {Object} Statistik yang siap ditampilkan.
 */
export function calculateQuestionStatistics(questions) {
  if (!questions || questions.length === 0) {
    return {
      total_questions: 0,
      question_types: {},
      difficulty: {},
      language: {},
      provider: null,
    };
  }

  const total = questions.length;
  const types = {};
  const difficulties = {};
  const languages = {};

  questions.forEach((q) => {
    // Tipe soal
    const type = q.type || "unknown";
    types[type] = (types[type] || 0) + 1;

    // Kesulitan (jika ada)
    if (q.difficulty) {
      difficulties[q.difficulty] = (difficulties[q.difficulty] || 0) + 1;
    }

    // Bahasa (jika ada, mungkin dari metadata atau field language)
    const lang = q.language || q.metadata?.language;
    if (lang) {
      languages[lang] = (languages[lang] || 0) + 1;
    }
  });

  // Provider bisa diambil dari luar karena tidak melekat pada tiap soal.
  // Untuk sekarang kita kembalikan null; bisa diisi oleh pemanggil.
  return {
    total_questions: total,
    question_types: types,
    difficulty: difficulties,
    language: languages,
    provider: null, // akan diisi oleh komponen yang tahu provider (dari respons generasi)
  };
}
