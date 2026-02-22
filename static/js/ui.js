/**
 * small UI helper functions (toast + header status)
 */

import { clearAuth, getUsername, isLoggedIn } from "./auth.js";

// simple HTML escaping to prevent XSS in the UI (we should use a library for this in production)
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// update the header based on login status
export function renderHeader() {
  const nav = document.getElementById("navLinks");
  const status = document.getElementById("authStatus");

  if (!nav || !status) return;

  if (isLoggedIn()) {
    nav.innerHTML = `
      <a href="/">List</a>
      <a href="/create">Create</a>
    `;

    const username = getUsername() || "user";
    status.innerHTML = `
      <span class="small">Logged in as <b>${escapeHtml(username)}</b></span>
      <button id="logoutBtn" style="margin-left:10px;">Logout</button>
    `;

    document.getElementById("logoutBtn").addEventListener("click", () => {
      clearAuth();
      window.location.href = "/login";
    });
  } else {
    nav.innerHTML = `
      <a href="/">List</a>
      <a href="/create">Create</a>
      <a href="/login">Login</a>
      <a href="/signup">Sign Up</a>
    `;

    status.innerHTML = `<span class="small">Not logged in</span>`;
  }
}

// show a toast message (simple alert that disappears after 3 seconds)
export function showToast(message) {
  const host = document.getElementById("toast");
  if (!host) return;

  host.textContent = message;
  host.classList.add("toast");
  setTimeout(() => {
    host.classList.remove("toast");
  }, 3000);
}

