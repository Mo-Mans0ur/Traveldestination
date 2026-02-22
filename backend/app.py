from flask import Flask, request, jsonify, render_template
from db import init_db, get_db_connection, now_iso
from auth import hash_password, verify_password, generate_token, require_auth


# Initialize the Flask application
app = Flask(__name__, template_folder="../templates",
            static_folder="../static")
# makes sure the database is initialized when the app starts
init_db()


############################
# FRONTEND ROUTES
############################

"""list over destinations"""


@app.route("/")
def page_index():
    try:
        return render_template("index.html", title="Travel Destinations")
    except Exception as e:
        print("ERROR in /:", e, flush=True)
        return "system under maintenance", 500


############################
"""This route is for the create page, which is a form to create a new travel destination."""


@app.route("/create")
def page_create():
    try:
        return render_template("create.html", title="Create Travel Destination")
    except Exception as e:
        print("ERROR in /create:", e, flush=True)
        return "system under maintenance", 500


############################
"""This route is for the edit page, which is a form to edit an existing travel destination."""


@app.route("/edit")
def page_edit():
    try:
        return render_template("edit.html", title="Edit Travel Destination")
    except Exception as e:
        print("ERROR in /edit:", e, flush=True)
        return "system under maintenance", 500


############################
"""This route is for the login page, which is a form to log in."""


@app.route("/login")
def page_login():
    try:
        return render_template("login.html", title="Login")
    except Exception as e:
        print("ERROR in /login:", e, flush=True)
        return "system under maintenance", 500


############################
"""This route is for the signup page, which is a form to register a new user."""


@app.route("/signup")
def page_signup():
    try:
        return render_template("signup.html", title="Sign Up")
    except Exception as e:
        print("ERROR in /signup:", e, flush=True)
        return "system under maintenance", 500


#################
# AUTH API
#################

"""
creates a new user account with the provided username and password.
the password is hashed using the hash_password function before being stored in the database.

"""


@app.post("/api/auth/signup")
def api_signup():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (%s, %s, %s)",
            (username, hash_password(password), now_iso())
        )

        conn.commit()
        user_id = cursor.lastrowid
        token = generate_token(user_id)
        return jsonify({"message": "User created successfully", "token": token}), 201

    except Exception as e:
        print("ERROR in /api/auth/signup:", e, flush=True)
        if "UNIQUE constraint failed: users.username" in str(e):
            return jsonify({"error": "Username already exists"}), 409
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


##############################
"""
verifies the provided username and password against the stored hash in the database.
if the credentials are valid, it generates and returns a token for the user.

"""


@app.post("/api/auth/login")
def api_login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    if not verify_password(user["password_hash"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_token(user["id"])
    return jsonify({"message": "Login successful", "token": token, "username": user["username"]}), 200


#################
# DESTINATIONS API
#################

"""
This route retrieves a list of all travel destinations from the database 

"""


@app.get("/api/destinations")
@require_auth
def api_list_destinations(user_id):
    # returns all the destinations for the authenticated user

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """SELECT * FROM destinations WHERE user_id = %s ORDER BY created_at DESC""", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    # Convert the rows to a list of dictionaries
    destinations = [dict(r) for r in rows]
    return jsonify(destinations), 200


###################################
"""
This route creates a new travel destination with the provided data in the request body.
backend validation

"""


@app.post("/api/destinations")
@require_auth
def api_create_destination(user_id):
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    date_from = data.get("date_from", "").strip()
    date_to = data.get("date_to", "").strip()
    description = data.get("description", "").strip()
    location = data.get("location", "").strip()
    country = data.get("country", "").strip()

    if not title or not date_from or not date_to or not location or not country:
        return jsonify({"error": "Title, date_from, date_to, location, and country are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    datetime = now_iso()
    try:
        cursor.execute("""INSERT INTO destinations 
                       (name, date_from, date_to, description, location, country, user_id, created_at, updated_at) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (title, date_from, date_to, description, location, country, user_id, datetime, datetime))

        conn.commit()
        destination_id = cursor.lastrowid

        return jsonify({"message": "Destination created successfully", "destination_id": destination_id}), 201
    except Exception as e:
        return jsonify({"error": "Failed to create destination"}), 500
    finally:
        conn.close()


###############################
"""
this gets a specific destination by its ID, but only if it belongs to the authenticated user.
"""


@app.get("/api/destinations/<int:destination_id>")
@require_auth
def api_get_destination(user_id, destination_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """SELECT * 
        FROM destinations 
        WHERE id = %s AND user_id = %s
        """, (destination_id, user_id))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Destination not found"}), 404

    destination = dict(row)
    return jsonify(destination), 200


##############################
"""
this updates an existing destination by its ID, but only if it belongs to the authenticated user.
"""


@app.put("/api/destinations/<int:destination_id>")
@require_auth
def api_update_destination(user_id, destination_id):
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    date_from = data.get("date_from", "").strip()
    date_to = data.get("date_to", "").strip()
    description = data.get("description", "").strip()
    location = data.get("location", "").strip()
    country = data.get("country", "").strip()

    if not title or not date_from or not date_to or not location or not country:
        return jsonify({"error": "Title, date_from, date_to, location, and country are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """UPDATE destinations 
        SET name = %s, date_from = %s, date_to = %s, description = %s, location = %s, country = %s, updated_at = %s
        WHERE id = %s AND user_id = %s""",
        (title, date_from, date_to, description, location,
         country, now_iso(), destination_id, user_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()

    if updated == 0:
        return jsonify({"error": "Destination not found or not owned by user"}), 404

    return jsonify({"message": "Destination updated successfully"}), 200


#############################
"""
this deletes an existing destination by its ID.

the frontend should show:
- delete button only if logged in
- confirmation dialog before deleting
- remove the element from the ui without refresh
"""


@app.delete("/api/destinations/<int:destination_id>")
@require_auth
def api_delete_destination(user_id, destination_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """DELETE FROM destinations 
        WHERE id = %s AND user_id = %s""",
        (destination_id, user_id)
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Destination not found or not owned by user"}), 404

    return jsonify({"message": "Destination deleted successfully"}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
