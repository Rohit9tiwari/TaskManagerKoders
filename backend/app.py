from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_connection, init_db

app = Flask(__name__)
CORS(app)

init_db()

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (data["title"], data.get("description", ""))
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task created"}), 201


@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "completed": bool(row["completed"])
        })

    return jsonify(tasks)


@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title=?, description=? WHERE id=?",
        (data.get("title"), data.get("description"), id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task updated"})


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted"})


@app.route("/tasks/<int:id>/toggle", methods=["PATCH"])
def toggle_task(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET completed = NOT completed WHERE id=?",
        (id,)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Status updated"})

if __name__ == "__main__":
    app.run(debug=True)
