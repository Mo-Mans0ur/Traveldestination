import { apiFetch } from "../api";
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

signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = signupForm.elements["username"].value.trim();
    const password = signupForm.elements["password"].value.trim();

    try {
        const res = await handleSignup(username, password);
        setAuth(res.token, res.username);
        showToast("Signup successful");
        window.location.href = "/index.html";
    } catch (error) {
        showToast("Signup failed: " + error.message);
    }
});

