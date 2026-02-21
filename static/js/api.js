/**
 makes a wrapper so we avoid repeating the same code for fetching 
 and error handling in all our API calls 

pros:
- same error handling in all API calls
- same JSON parsing in all API calls
- automatically adds the auth token if it exists


 */

import { getToken } from "./auth.js";

export async function apiFetch(
  path,
  { method = "GET", body = null, auth = true } = {},
) {
  const headers = {
    "Content-Type": "application/json",
  };

  // if we need auth, then we send the token with
  if (auth) {
    const token = getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }

  // make the API call
  try {
    const response = await fetch(path, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }

    return await response.json();
  } catch (error) {
    console.error("API call failed:", error);
    throw error;
  }

  // try to read JSON (some responses could be empty)
  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const errorMessage =
      data?.error || "An error occurred" + ` (status: ${response.status})`;
    throw new Error(errorMessage);
  }

  return data;
}
