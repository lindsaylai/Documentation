document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".tutor-snippet").forEach((snippet) => {
    const button = snippet.querySelector(".tutor-snippet__copy");
    if (!button) {
      return;
    }

    button.addEventListener("click", async (event) => {
      event.preventDefault();
      event.stopPropagation();

      const code = snippet.querySelector("pre code");
      const text = code ? code.textContent : "";
      if (!text) {
        return;
      }

      try {
        await navigator.clipboard.writeText(text);
      } catch {
        const field = document.createElement("textarea");
        field.value = text;
        field.setAttribute("readonly", "");
        field.style.position = "fixed";
        field.style.left = "-9999px";
        document.body.appendChild(field);
        field.select();
        document.execCommand("copy");
        field.remove();
      }

      button.classList.add("is-copied");
      button.setAttribute("aria-label", "Copied tutor text");
      window.setTimeout(() => {
        button.classList.remove("is-copied");
        button.setAttribute("aria-label", "Copy tutor text");
      }, 1600);
    });
  });
});
