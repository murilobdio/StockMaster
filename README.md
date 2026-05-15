# 📦 StockMaster

Sistema corporativo para gerenciamento de ativos e suporte técnico.

Desenvolvido com:

- Python
- Flask
- SQLite
- HTML/CSS/JavaScript

---

# 🚀 Funcionalidades

## ✅ Gestão de ativos
- Cadastro de ativos
- Edição de ativos
- Exclusão de ativos
- Controle de categoria
- Controle de status
- Registro de última falha

## ✅ Sistema de suporte
- Abertura de tickets
- Níveis de criticidade:
  - N1 (Baixa)
  - N2 (Média)
  - N3 (Alta)
- Controle de status:
  - Ticket aberto
  - Em manutenção
  - Finalizado

## ✅ Interface moderna
- Layout responsivo
- Design corporativo estilo dashboard
- Cards organizados
- Interface leve e intuitiva

---

# 🖥️ Tecnologias utilizadas

| Tecnologia | Uso |
|------------|-----|
| Python | Backend |
| Flask | API / Web Server |
| SQLite | Banco de dados local |
| HTML | Estrutura da interface |
| CSS | Estilização |
| JavaScript | Interatividade |

---

# 📂 Estrutura do projeto

```
project/
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── img/
│       └── bg.jpg
│
├── app.py
├── main.py
├── database.db
├── requirements.txt
└── README.md
```

---

# ▶️ Como executar o projeto

## 1. Clonar o repositório

git clone https://github.com/murilobdio/StockMaster.git

Entrar na pasta:

cd NOME_DO_REPOSITORIO

---

## 2. Instalar dependências

pip install flask


---

## 3. Executar o sistema

python launcher.py


---

## 4. Acessar no navegador

http://127.0.0.1:5000

---

# ⚠️ Observações importantes

- O banco SQLite (`database.db`) é criado automaticamente.
- O sistema será aberto automaticamente no navegador.
- Para encerrar: CTRL + C
