/* Dr Neal Aggarwal — main.js */

// ── Mobile nav toggle ────────────────────────────────────────────────────
const toggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');
if (toggle && navLinks) {
  toggle.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// ── Active nav link ──────────────────────────────────────────────────────
const path = window.location.pathname;
document.querySelectorAll('.nav-links a').forEach(a => {
  const href = a.getAttribute('href');
  if (href === path || (href !== '/' && path.startsWith(href))) {
    a.classList.add('active');
  }
});

// ── Animate skill bars on scroll ─────────────────────────────────────────
function animateBars() {
  document.querySelectorAll('.level-bar__fill[data-width]').forEach(el => {
    const rect = el.closest('.level-bar').getBoundingClientRect();
    if (rect.top < window.innerHeight - 40) {
      el.style.width = el.dataset.width + '%';
      el.removeAttribute('data-width');
    }
  });
}

// Set initial width to 0 so animation plays
document.querySelectorAll('.level-bar__fill').forEach(el => {
  el.dataset.width = el.style.width || '70';
  el.style.width = '0';
});

window.addEventListener('scroll', animateBars, { passive: true });
animateBars();

// ── Statusbar clock ──────────────────────────────────────────────────────
const clock = document.getElementById('statusbar-time');
if (clock) {
  function tick() {
    const now = new Date();
    clock.textContent = now.toUTCString().replace('GMT', 'UTC');
  }
  tick();
  setInterval(tick, 1000);
}
