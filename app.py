from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import sqlite3
from datetime import datetime, time

def get_db_connection():
    conn = sqlite3.connect("alumnos.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to the API"})

@app.route("/base", methods=["GET"])
def base():
    return render_template('base.html')

@app.route("/home", methods=["GET"])
def home():
    return render_template('home.html')

@app.route("/about", methods=["GET"])
def about():
    return render_template('about.html')

@app.route("/post", methods=["GET"])
def get_all_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM alumnos').fetchall()
    conn.close()
    posts_lists = [dict(post) for post in posts]
    return jsonify(posts_lists)

@app.route("/post/<int:post_id>", methods=["GET"])
def get_one_post(post_id: int):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM alumnos WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404, description="Post not found")
    return jsonify(dict(post))


@app.route("/post/create", methods=["POST"])
def create_one_post():
    data = request.json
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    aprobado = data.get('aprobado')
    nota = data.get('nota')
    fecha = datetime.now()
    
    conn = get_db_connection()
    conn.execute('INSERT INTO alumnos (nombre, apellido, aprobado, nota, fecha) VALUES (?, ?, ?, ?, ?)', (nombre, apellido, aprobado, nota, fecha))
    conn.commit()
    conn.close()
    return jsonify({"message": "Post created"})


@app.route("/post/edit/<int:post_id>", methods=["PUT"])
def edit_one_post(post_id):
    data = request.json
    nombre = data.get('nombre')
    nota = data.get('nota')

    conn = get_db_connection()
    conn.execute('UPDATE posts SET nombre = ?, nota = ? WHERE id = ?', (nombre, nota, post_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Post updated"})


@app.route("/post/delete/<int:post_id>", methods=["POST"])
def delete_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM alumnos WHERE id = ?', (post_id,)).fetchone()
    
    if post is None:
        abort(404)

    conn.execute('DELETE FROM alumnos WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('get_all_posts'))


# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, port=5000)
