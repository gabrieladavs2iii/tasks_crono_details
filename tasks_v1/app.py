from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Inicializar base de datos
def init_db():
    conn = sqlite3.connect("tareas.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tareas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    responsable TEXT,
                    tarea TEXT,
                    dias INTEGER,
                    porcentaje INTEGER
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/tareas", methods=["GET"])
def get_tareas():
    conn = sqlite3.connect("tareas.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tareas")
    rows = c.fetchall()
    conn.close()
    # Convertir a lista de diccionarios
    tareas = [{"id": r[0], "responsable": r[1], "tarea": r[2], "dias": r[3], "porcentaje": r[4]} for r in rows]
    return jsonify(tareas)

@app.route("/api/tareas", methods=["POST"])
def add_tarea():
    try:
        data = request.get_json(force=True)  # fuerza a leer JSON
        responsable = data.get("responsable", "")
        tarea = data.get("tarea", "")
        dias = int(data.get("dias", 0))
        porcentaje = int((dias / 5) * 100)

        conn = sqlite3.connect("tareas.db")
        c = conn.cursor()
        c.execute("INSERT INTO tareas (responsable, tarea, dias, porcentaje) VALUES (?, ?, ?, ?)",
                  (responsable, tarea, dias, porcentaje))
        conn.commit()
        conn.close()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/tareas/<int:id>", methods=["DELETE"])
def delete_tarea(id):
    conn = sqlite3.connect("tareas.db")
    c = conn.cursor()
    c.execute("DELETE FROM tareas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
