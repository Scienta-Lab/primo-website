const root = document.documentElement;
const body = document.body;
const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');
const themeToggle = document.querySelector('[data-theme-toggle]');
const announcement = document.querySelector('[data-announcement]');
const closeAnnouncement = document.querySelector('[data-close-announcement]');

const storedTheme = localStorage.getItem('primo-theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
if (storedTheme === 'dark' || (!storedTheme && prefersDark)) {
  root.dataset.theme = 'dark';
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const dark = root.dataset.theme === 'dark';
    if (dark) {
      delete root.dataset.theme;
      localStorage.setItem('primo-theme', 'light');
      themeToggle.setAttribute('aria-label', 'Toggle dark theme');
    } else {
      root.dataset.theme = 'dark';
      localStorage.setItem('primo-theme', 'dark');
      themeToggle.setAttribute('aria-label', 'Toggle light theme');
    }
  });
}

if (sessionStorage.getItem('primo-announcement-closed') === 'true' && announcement) {
  announcement.hidden = true;
  body.classList.add('announcement-closed');
}

if (closeAnnouncement && announcement) {
  closeAnnouncement.addEventListener('click', () => {
    announcement.hidden = true;
    body.classList.add('announcement-closed');
    sessionStorage.setItem('primo-announcement-closed', 'true');
  });
}

if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const open = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!open));
    nav.classList.toggle('is-open', !open);
  });

  nav.addEventListener('click', (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      navToggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) {
      navToggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    }
  });
}
