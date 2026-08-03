/**
 * Menyalin teks ke clipboard.
 * @param {string} text - Teks yang akan disalin.
 * @returns {Promise<boolean>} - true jika berhasil, false jika gagal.
 */
export async function copyToClipboard(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    }
    // Fallback
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    const success = document.execCommand("copy");
    document.body.removeChild(textarea);
    return success;
  } catch (err) {
    console.error("Clipboard copy failed:", err);
    return false;
  }
}
