import threading
import webbrowser
import os
import sys
from app import app, init_db

# ---------- Caminho base (para compatibilidade com PyInstaller) ----------
def caminho_base():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(".")

BASE_DIR = caminho_base()

# ---------- Função para abrir navegador ----------
def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000")

# ---------- Função principal ----------
def main():
    # Inicializa o banco
    init_db()

    # Abre o navegador após 1 segundo (thread separada)
    threading.Timer(1.0, abrir_navegador).start()

    # Roda o Flask
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    main()