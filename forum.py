from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS User_Data")
    cursor.execute("""
        CREATE TABLE User_Data (
            groceries FLOAT,
            entertainment FLOAT,
            utilities FLOAT,
            actual_savings FLOAT,
            predicted_saving FLOAT,
            suggestion VARCHAR(255)
        )
    """)
    conn.commit()
    conn.close()

    # Home route for the forum page
@app.route("/")
def forum():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, task, status FROM Tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("forum.html", tasks=tasks)

# Route to add a new task
@app.route("/add_task", methods=["POST"])
def add_task():
    username = request.form["username"]
    task = request.form["task"]
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tasks (username, task, status) VALUES (?, ?, ?)", (username, task, "Pending"))
    conn.commit()
    conn.close()
    return redirect(url_for("forum"))

# Route to mark a task as completed
@app.route("/complete_task/<int:task_id>")
def complete_task(task_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("forum"))

# Route to delete a task
@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("forum"))

if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True)

