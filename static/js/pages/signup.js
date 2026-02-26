import { apiFetch } from "../api.js";
import { renderHeader, showToast } from "../ui.js";
import { setAuth } from "../auth.js";

// render the header with the auth status
renderHeader();

//makes a user and saves the token in localStorage
async function handleSignup(username, password) {
  return apiFetch("/api/auth/signup", {
    method: "POST",
    body: { username, password },
    auth: false, // no need to send the token for signup
  });
}

// handle the form submission to sign up
const signupForm = document.getElementById("signup-form");
const usernameInput = signupForm.elements["username"];
const usernameStatus = document.getElementById("username-status");

let usernameCheckTimeout = null;

// Debounced live username validation & availability check
usernameInput.addEventListener("input", () => {
  const value = usernameInput.value.trim();

  // Clear previous timer
  if (usernameCheckTimeout) clearTimeout(usernameCheckTimeout);

  if (!value) {
    usernameStatus.textContent = "";
    usernameStatus.dataset.state = "";
    return;
  }

  usernameStatus.textContent = "Checking username...";
  usernameStatus.dataset.state = "checking";

  usernameCheckTimeout = setTimeout(async () => {
    try {
      const res = await apiFetch(
        `/api/auth/check-username?username=${encodeURIComponent(value)}`,
        {
          method: "GET",
          auth: false,
        },
      );

      if (!res.valid) {
        usernameStatus.textContent = res.error || "Invalid username";
        usernameStatus.dataset.state = "invalid";
      } else if (!res.available) {
        usernameStatus.textContent = "Username is already taken";
        usernameStatus.dataset.state = "taken";
      } else {
        usernameStatus.textContent = "Username is available";
        usernameStatus.dataset.state = "ok";
      }
    } catch (error) {
      usernameStatus.textContent = "Could not check username";
      usernameStatus.dataset.state = "error";
    }
  }, 500); // 500ms debounce
});

signupForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = signupForm.elements["username"].value.trim();
  const password = signupForm.elements["password"].value.trim();

  try {
    const res = await handleSignup(username, password);
    setAuth(res.token, res.username);
    showToast("Signup successful");
    window.location.href = "/";
  } catch (error) {
    showToast("Signup failed: " + error.message);
  }
});
