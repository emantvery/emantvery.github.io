const root = document.documentElement;
const toggle = document.querySelector(".theme-toggle");
let savedTheme = null;
try { savedTheme = localStorage.getItem("portfolio-theme"); } catch {}
root.dataset.theme = savedTheme || (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
toggle?.addEventListener("click", () => {
  const next = root.dataset.theme === "dark" ? "light" : "dark";
  root.dataset.theme = next;
  try { localStorage.setItem("portfolio-theme", next); } catch {}
});

const menu = document.querySelector(".menu-toggle");
const nav = document.querySelector("#site-nav");
const closeMenu = () => {
  nav?.classList.remove("is-open");
  menu?.setAttribute("aria-expanded", "false");
};
menu?.addEventListener("click", () => {
  const open = nav?.classList.toggle("is-open") ?? false;
  menu.setAttribute("aria-expanded", String(open));
});
nav?.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeMenu();
});
