import { requireLogin } from "../auth.js";
import { renderHeader, showToast } from "../ui.js";
import {
  createDestination,
  getDestination,
  updateDestination,
} from "../destinations.js";

// make sure the user is logged in to access this page
requireLogin();

// render the header with the auth status
renderHeader();

// handle the form submission to create a new destination
const form = document.getElementById("edit-form");

// reads the ?id= from the url
//this page only works if there's an id with
function getDestinationIdFromQuery() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");
  // IDs are UUID strings from the backend, so just return as-is
  return id || null;
}

// fills the form with the destination data
function fillForm(destination) {
  form.elements["title"].value = destination.name;
  form.elements["date_from"].value = destination.start_date;
  form.elements["date_to"].value = destination.end_date;
  form.elements["country"].value = destination.country;
  form.elements["location"].value = destination.location;
  form.elements["description"].value = destination.description;
}

//reads the form data and makes a payload object to send to the API
function readFormData() {
  const fd = new FormData(form); //if it dont work delete this and do it manually with form.elements["fieldname"].value
  return {
    title: fd.get("title"),
    date_from: fd.get("date_from"),
    date_to: fd.get("date_to"),
    country: fd.get("country").trim(),
    location: fd.get("location").trim(),
    description: fd.get("description").trim(),
  };
}

// Frontend validation: just like in create.js
function validateFormData(payload) {
  if (!payload.title) {
    return showToast("Title is required");
  }

  if (
    payload.date_from &&
    payload.date_to &&
    payload.date_from > payload.date_to
  ) {
    return showToast("Start date cannot be after or equal to end date");
  }

  return null;
}

// get id from query
const id = getDestinationIdFromQuery();
if (!id) {
  showToast("missing id in query string. Example: ?id=some-id");
  form.style.display = "none";
} else {
  // load the destination data and fill the form
  tryLoad(id);
}

async function tryLoad(id) {
  try {
    const destination = await getDestination(id);
    fillForm(destination);
  } catch (error) {
    showToast("Failed to load destination: " + error.message);
  }
}

// handle the form submission to update the destination
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = readFormData();
  const validationError = validateFormData(payload);
  if (validationError) {
    showToast(validationError);
    return;
  }

  try {
    await updateDestination(id, payload);
    showToast("Destination updated successfully");
    window.location.href = "/";
  } catch (error) {
    showToast("Failed to update destination: " + error.message);
  }
});
