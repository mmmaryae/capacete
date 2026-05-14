from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# ==============================================================
# 🚨 CONFIGURAÇÃO INTELIGENTE DO BANCO DE DADOS
# ==============================================================
# Pega a URL do Render. Se não achar (rodando no seu PC), usa o SQLite padrão.
banco_url = os.getenv('DATABASE_URL', 'sqlite:///camcore.db')

# O macete obrigatório para o Render (corrige o nome do postgres)
if banco_url.startswith("postgres://"):
    banco_url = banco_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = banco_url
# ==============================================================

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# --- CONFIGURAÇÃO DE E-MAIL (MAILTRAP) ---
# Servidor e porta não são dados sensíveis, podem ficar no código
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Credenciais sensíveis puxadas do .env
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') 
# ----------------------------------------------

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = "login" 

mail = Mail(app)

from CamCore import routes, models

with app.app_context():
    database.create_all()