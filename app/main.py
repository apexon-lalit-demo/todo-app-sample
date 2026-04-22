"""Todo List Web App — sample app for Vibe Coder deployment."""

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

todos: dict[str, dict] = {}


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "todo-app"})


@app.route("/")
def index():
    sorted_todos = sorted(todos.values(), key=lambda t: t["created_at"], reverse=True)
    return render_template("index.html", todos=sorted_todos)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        tid = str(uuid.uuid4())[:8]
        todos[tid] = {
            "id": tid,
            "title": title,
            "done": False,
            "created_at": datetime.utcnow().isoformat(),
        }
    return redirect(url_for("index"))


@app.route("/toggle/<tid>")
def toggle(tid):
    if tid in todos:
        todos[tid]["done"] = not todos[tid]["done"]
    return redirect(url_for("index"))


@app.route("/delete/<tid>")
def delete(tid):
    todos.pop(tid, None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
