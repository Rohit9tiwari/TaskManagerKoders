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
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Check if task exists
    cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = cursor.fetchone()
    if not task:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    # Build update query dynamically
    updates = []
    params = []
    if "title" in data and data["title"] is not None:
        updates.append("title=?")
        params.append(data["title"])
    if "description" in data and data["description"] is not None:
        updates.append("description=?")
        params.append(data["description"])
    if "completed" in data and data["completed"] is not None:
        updates.append("completed=?")
        params.append(1 if data["completed"] else 0)

    if not updates:
        conn.close()
        return jsonify({"error": "No valid fields to update"}), 400

    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id=?"
    params.append(id)

    cursor.execute(query, params)
    conn.commit()
    conn.close()

    return jsonify({"message": "Task updated"})


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = cursor.fetchone()
    if not task:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted"})


@app.route("/tasks/<int:id>/toggle", methods=["PATCH"])
def toggle_task(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = cursor.fetchone()
    if not task:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    cursor.execute(
        "UPDATE tasks SET completed = NOT completed WHERE id=?",
        (id,)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Status updated"})

if __name__ == "__main__":
    app.run(debug=True)
