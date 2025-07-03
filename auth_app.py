import sqlite3, hashlib
from flask import Flask, request
DB = "usuarios.db"
USUARIOS = [("Jesus","jesus123"), ("Tomas","saldias456"), ("alvasaldi","toje789")]
hashpw = lambda p: hashlib.sha256(p.encode()).hexdigest()

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)")
    for u,p in USUARIOS:
        try:
            cur.execute("INSERT INTO users VALUES(?,?)", (u, hashpw(p)))
        except sqlite3.IntegrityError:
            pass
    con.commit(); con.close()

app = Flask(__name__)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        con = sqlite3.connect(DB); cur = con.cursor()
        cur.execute("SELECT password FROM users WHERE username=?", (u,))
        fila = cur.fetchone(); con.close()
        if fila and fila[0] == hashpw(p):
            return f"<h2>Bienvenido {u}</h2>", 200
        return "<h3>Error de usuario o contraseña</h3>", 401
    return '''<form method="POST">
                Usuario: <input name="username"><br>
                Clave: <input type="password" name="password"><br>
                <button>Entrar</button></form>'''

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5800)

