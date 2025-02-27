from flask import Flask, request, redirect, render_template, g
from lib.db import Database

db_handler = Database()

app = Flask(__name__, template_folder="templates")

@app.before_request
def before_request():
    g.db = db_handler.get_connection()

@app.teardown_appcontext
def teardown_db(exception):
    db_handler.close_connection()

@app.route("/", methods=["GET"])
def home_route():
    db = g.db
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    return render_template("home.html", users=users)

@app.route("/create-profile", methods=["GET"])
def new_users():
    return render_template("new_users.html")

@app.route("/edit-profile/<id>", methods=["GET"]) 
def edit_user(id):
    db = g.db
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    return render_template("edit_user.html", user=user)

@app.route("/create-profile", methods=["POST"])
def create_profile():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    role = request.form.get("role", "").strip()

    db = g.db
    cursor = db.cursor()

    if not name or not email or not role:
        return redirect("/create-profile")

    cursor.execute('''
        INSERT INTO users (name, email, role) VALUES (?, ?, ?)
    ''', (name, email, role))

    db.commit()
    return redirect("/")


@app.route("/update-user/<id>", methods=["PUT"])
def update_user(id: str):
    user = request.get_json() 
    db = g.db
    cursor = db.cursor()

    cursor.execute('''
        UPDATE users SET name = ?, role = ? WHERE id = ?               
    ''', (user["name"], user["role"], id))

    db.commit()
    return redirect("/")

@app.route("/delete-user/<id>", methods=["DELETE"])
def delete_user(id: str):
    db = g.db
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    db.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
