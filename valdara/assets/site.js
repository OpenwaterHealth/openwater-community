// Mobile nav
const toggle = document.querySelector(".nav-toggle");
const links = document.querySelector(".nav-links");
if (toggle && links) {
  toggle.addEventListener("click", () => links.classList.toggle("open"));
}

// Scroll reveal
const io = new IntersectionObserver(
  (entries) => {
    for (const e of entries) {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        io.unobserve(e.target);
      }
    }
  },
  { threshold: 0.12 }
);
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

// Interest registry form (front-end only — no backend wired yet)
document.querySelectorAll("form.reg-form").forEach((form) => {
  form.addEventListener("submit", (ev) => {
    ev.preventDefault();
    const status = form.querySelector(".form-status");
    if (status) {
      status.textContent =
        "Thank you. Your interest has been recorded and you will receive development updates from Valdara.";
    }
    form.querySelectorAll("input, select, button").forEach((el) => (el.disabled = true));
  });
});
