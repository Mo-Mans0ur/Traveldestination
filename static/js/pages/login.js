import { apiFetch } from "../api.js";
import { renderHeader, showToast } from "../ui.js";
import { setAuth } from "../auth.js";

// render the header with the auth status
renderHeader();

// handle the form submission to log in
const loginForm = document.getElementById("login-form");

// logging in via the API and saving the token in localStorage
async function handleLogin(username, password) {
    return apiFetch("/api/auth/login", {
        method: "POST",
        body: { username, password },
        auth: false, // no need to send the token for login
    });
}

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = loginForm.elements["username"].value.trim();
    const password = loginForm.elements["password"].value.trim();


    try {
        const res = await handleLogin(username, password);
        setAuth(res.token, res.username);
        showToast("Login successful");
        window.location.href = "/";
    } catch (error) {
        showToast("Login failed: " + error.message);
    }
});