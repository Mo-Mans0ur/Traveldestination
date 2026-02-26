import { requireLogin, isLoggedIn } from "../auth.js";
import { renderHeader, showToast } from "../ui.js";
import { listDestinations, deleteDestination } from "../destinations.js";

// make sure the user is logged in to access this page
requireLogin();

// render the header with the auth status
renderHeader();

//load the destinations and render them in the list
const listEl = document.getElementById("list");

async function loadDestinations() {
  try {
    const destinations = await listDestinations();
    renderList(destinations);
  } catch (error) {
    showToast("Failed to load destinations: " + error.message);
  }
}

// render the list of destinations in the UI
function renderList(destinations) {
  listEl.innerHTML = "";

  if (destinations.length === 0) {
    listEl.innerHTML =
      "<div>No destinations yet. Click 'Add Destination' to create one.</div>";
    return;
  }

  for (const dest of destinations) {
    const card = document.createElement("div");
    card.className = "card";
    card.dataset.id = dest.destination_id;

    const dates = formatDateRange(dest.date_from, dest.date_to);

    card.innerHTML = `
            <h3>${escapeHtml(dest.name)}</h3>
            <div class="small">${escapeHtml(dest.country)} ${escapeHtml(dest.location)}</div>
            <div class="small">${escapeHtml(dates)}</div>
            <p>${escapeHtml(dest.description || "")}</p>

            <div class="actions">
                <button class="editBtn">Edit</button>
                ${isLoggedIn() ? `<button class="deleteBtn">Delete</button>` : ""}
            </div>
        `;
    // edit button: sends the user to the edit page with the destination id in the query string
    card.querySelector(".editBtn").addEventListener("click", () => {
      window.location.href = `/edit?id=${dest.destination_id}`;
    });

    // delete button: calls the API to delete the destination and removes it from the UI only if the user is logged in
    const deleteBtn = card.querySelector(".deleteBtn");
    if (deleteBtn) {
      deleteBtn.addEventListener("click", async () => {
        if (confirm("Are you sure you want to delete this destination?")) {
          try {
            await deleteDestination(dest.destination_id);
            card.remove();
            showToast("Deleted ✔");
          } catch (error) {
            showToast("Failed to delete destination: " + error.message);
          }
        }
      });
    }

    listEl.appendChild(card);
  }
}

// this function is used to escape HTML special characters to prevent XSS attacks
// when rendering user-generated content in the UI. It replaces &, <, >, ",
// and ' with their corresponding HTML entities.
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatDate(dateStr) {
  if (!dateStr) return "";

  const date = new Date(dateStr);
  if (Number.isNaN(date.getTime())) {
    // If parsing fails, fall back to the original string
    return String(dateStr);
  }

  return date.toLocaleDateString(undefined, {
    weekday: "short",
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function formatDateRange(from, to) {
  const fromFormatted = formatDate(from);
  const toFormatted = formatDate(to);

  if (fromFormatted && toFormatted) return `${fromFormatted} to ${toFormatted}`;
  if (fromFormatted) return fromFormatted;
  if (toFormatted) return toFormatted;

  return "Dates not set";
}

// load the destinations when the page loads
if (!listEl) {
  showToast('Missing element: id="list" in the index.html');
} else {
  loadDestinations();
}
