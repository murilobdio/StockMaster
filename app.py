import sys
import os
import sqlite3
from flask import Flask, request, jsonify, render_template

# ---------- Caminho base ----------
def caminho_base():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(".")

BASE_DIR = caminho_base()

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

DB_NAME = os.path.join(BASE_DIR, "database.db")

# ---------- DB ----------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ativos (
            id_ativo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_ativo TEXT NOT NULL,
            tipo_categoria TEXT,
            data_aquisicao DATE,
            status_governanca TEXT,
            ultima_falha DATETIME
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
            id_ativo INTEGER,
            nivel_criticidade TEXT,
            descricao_erro TEXT,
            status_suporte TEXT,
            FOREIGN KEY (id_ativo) REFERENCES ativos(id_ativo)
        )
    ''')

    conn.commit()
    conn.close()

# ---------- ROTAS ----------
@app.route("/")
def index():
    return render_template("index.html")

# -------- ATIVOS --------
@app.route("/ativos", methods=["GET"])
def listar_ativos():
    conn = get_db()
    dados = conn.execute("SELECT * FROM ativos").fetchall()
    conn.close()
    return jsonify([dict(d) for d in dados])

@app.route("/ativos", methods=["POST"])
def adicionar_ativo():
    data = request.json
    conn = get_db()
    conn.execute('''
        INSERT INTO ativos (nome_ativo, tipo_categoria, data_aquisicao, status_governanca)
        VALUES (?, ?, ?, ?)
    ''', (
        data["nome_ativo"],
        data.get("tipo_categoria"),
        data.get("data_aquisicao"),
        data.get("status_governanca")
    ))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.route("/ativos/<int:id_ativo>", methods=["PUT"])
def atualizar_ativo(id_ativo):
    data = request.json
    conn = get_db()
    conn.execute('''
        UPDATE ativos
        SET nome_ativo=?, tipo_categoria=?, data_aquisicao=?, status_governanca=?
        WHERE id_ativo=?
    ''', (
        data["nome_ativo"],
        data.get("tipo_categoria"),
        data.get("data_aquisicao"),
        data.get("status_governanca"),
        id_ativo
    ))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.route("/ativos/<int:id_ativo>", methods=["DELETE"])
def deletar_ativo(id_ativo):
    conn = get_db()
    conn.execute("DELETE FROM ativos WHERE id_ativo=?", (id_ativo,))
    conn.commit()
    conn.close()
    return {"status": "ok"}

# -------- TICKETS --------
@app.route("/tickets", methods=["GET"])
def listar_tickets():
    conn = get_db()
    dados = conn.execute('''
        SELECT t.*, a.nome_ativo 
        FROM tickets t
        LEFT JOIN ativos a ON t.id_ativo = a.id_ativo
        WHERE t.status_suporte != 'Finalizado'
    ''').fetchall()
    conn.close()
    return jsonify([dict(d) for d in dados])

@app.route("/tickets", methods=["POST"])
def criar_ticket():
    data = request.json
    conn = get_db()
    conn.execute('''
        INSERT INTO tickets (id_ativo, nivel_criticidade, descricao_erro, status_suporte)
        VALUES (?, ?, ?, ?)
    ''', (
        data["id_ativo"],
        data["nivel_criticidade"],
        data["descricao_erro"],
        "Ticket aberto"
    ))

    # Atualiza última falha
    conn.execute('''
        UPDATE ativos
        SET ultima_falha = CURRENT_TIMESTAMP
        WHERE id_ativo = ?
    ''', (data["id_ativo"],))

    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.route("/tickets/<int:id_ticket>", methods=["PUT"])
def atualizar_status_ticket(id_ticket):
    data = request.json
    conn = get_db()
    conn.execute('''
        UPDATE tickets
        SET status_suporte=?
        WHERE id_ticket=?
    ''', (
        data["status_suporte"],
        id_ticket
    ))
    conn.commit()
    conn.close()
    return {"status": "ok"}

# ---------- INIT DB ----------
init_db()