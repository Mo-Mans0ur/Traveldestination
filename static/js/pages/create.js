import { requireLogin } from "../auth";
import { renderHeader, showToast } from "../ui";
import { createDestination } from "../destinations";

// make sure the user is logged in to access this page
requireLogin();

// render the header with the auth status
renderHeader();

// handle the form submission to create a new destination
const form = document.getElementById("create-form");

// reads the form data and makes a payload object to send to the API
function readFormData() {
    const fd = new FormData(form);
    return {
        title: fd.get("title"),
        Date_from: fd.get("date_from"),
        Date_to: fd.get("date_to"),
        country: fd.get("country"),
        location: fd.get("location"),
        description: fd.get("description"),
    };
}

// Frontend validation: check that the required fields are filled in
function validateFormData(payload) {
    if (!payload.title) {
        return showToast("Title is required");
    }
    if (payload.Date_from && payload.Date_to) {
        if (payload.Date_from > payload.Date_to) {
            return showToast("Start date cannot be after or equal to end date");
        }
    }

    return null;
}

// handle the form submission
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = readFormData();
    const validationError = validateFormData(payload);
    if (validationError) {
        showToast(validationError);
        return;
    }

    try {
        await createDestination(payload);
        showToast("Destination created successfully");
        window.location.href = "/index.html";
    } catch (error) {
        showToast("Failed to create destination: " + error.message);
    }
});