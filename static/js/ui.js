/**
 * small UI helper functions (toast + header status)
 */

import { clearAuth, getUsername, isLoggedIn } from "./auth.js";


// simple HTML escaping to prevent XSS in the UI (we should use a library for this in production)
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
 // render the header with the auth status (logged in as username + logout button)
export function renderHeader() {
  const el = document.getElementById("authStatus");
  if (!el) return;

  if (isLoggedIn()) {
    const username = getUsername() || "user";
    el.innerHTML = `
            <span class="small">Logged in as <b>${escapeHtml(username)}</b></span>
            <button id="logoutBtn" style="margin-left: 10px;">Logout</button>
        `;

    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        clearAuth();
        window.location.href = "/login.html";
      });
    } else {
      el.innerHTML += `<span style="color: red;">Not logged in</span>`;
    }
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
