from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, imya TEXT, prizvyshe TEXT, data_narodzhennya TEXT, nickneim TEXT, password TEXT)")
    conn.commit()
    conn.close()







@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nickneim = data['nickneim']
    klyuch_bezpeky = data['klyuch_bezpeky']

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE nickneim = ? AND password = ?", (nickneim, klyuch_bezpeky))
    user = cursor.fetchone()
    conn.close()


    if user:
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error"})








@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    imya = data["imya"]
    prizvyshe = data["prizvyshe"]
    data_narodzhennya = data["data_narodzhennya"]
    nickneim = data["nickneim"]
    klyuch_bezpeky = data["klyuch_bezpeky"]



    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (imya, prizvyshe, data_narodzhennya, nickneim, password) VALUES (?, ?, ?, ?, ?)", (imya, prizvyshe, data_narodzhennya, nickneim, klyuch_bezpeky))
    conn.commit()
    conn.close()


    return jsonify({"status": "ok"})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

















