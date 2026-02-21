/**
 * AUTH helper functions.
 * 
 * 
 * we use localStorage cause:
 * - it's simple to use
 * - the token survives page refreshes
 * - we don't need to worry about cookie security flags (HttpOnly, Secure, SameSite)
 * 
 */


const TOKEN_KEY = "travel_token";
const USERNAME_KEY = "travel_username";

// set the auth token in localStorage
export function setAuth(token, username) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USERNAME_KEY, username);
}

// remove the auth token from localStorage
export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USERNAME_KEY);
}

// get the auth token from localStorage
export function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

// get the username from localStorage
export function getUsername() {
    return localStorage.getItem(USERNAME_KEY);
}

// check if the user is logged in (i.e. has a token)
export function isLoggedIn() {
    return Boolean(getToken());
}

// if we want to secure a page:
// - if the user is not logged in, redirect to login page
export function requireLogin() {
    if (!isLoggedIn()) {
        window.location.href = "/login.html";
    }
}