const root = document.documentElement;
const toggle = document.querySelector(".theme-toggle");
const savedTheme = localStorage.getItem("portfolio-theme");
const preferredTheme = matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
root.dataset.theme = savedTheme || preferredTheme;
toggle?.addEventListener("click", () => {
  const next = root.dataset.theme === "dark" ? "light" : "dark";
  root.dataset.theme = next;
  localStorage.setItem("portfolio-theme", next);
});
