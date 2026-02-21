/**
 * Here we gather all api calls for destinations
 * this way it'll be easier to read.
 */

import { apiFetch } from "./api.js";


// list all destinations
export function listDestinations() {
    return apiFetch("/api/destinations", {
        method: "GET",
        auth: true,
    });
}

// create a new destination
export function createDestination(destination) {
    return apiFetch("/api/destinations", {
        method: "POST",
        body: destination,
        auth: true,
    });
}


//get a destination by id
export function getDestination(id) {
    return apiFetch(`/api/destinations/${id}`, {
        method: "GET",
        auth: true,
    });
}


// update a destination by id
export function updateDestination(id, payload) {
    return apiFetch(`/api/destinations/${id}`, {
        method: "PUT",
        body: payload,
        auth: true,
    });
}


// delete a destination by id
export function deleteDestination(id) {
    return apiFetch(`/api/destinations/${id}`, {
        method: "DELETE",
        auth: true,
    });
}