/**
 * Setiap formatter harus mengimplementasikan fungsi format(questions, metadata?) -> string.
 * Berikut adalah base class opsional (bisa diabaikan karena JS tidak strict).
 */
export class BaseFormatter {
  format(questions) {
    throw new Error("format() must be implemented");
  }
}
