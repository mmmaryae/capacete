
from CamCore import database, login_manager, app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_usuario(usuario_id):
    return Usuario.query.get(int(usuario_id))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha = database.Column(database.String(60), nullable=False)
    
    # Relação: Um usuário tem vários alertas. O backref cria a variável 'funcionario' no Alerta
    alertas = database.relationship('Alerta', backref='funcionario', lazy=True)
    def get_token_reset(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'usuario_id': self.id})

    @staticmethod
    def verificar_token_reset(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            usuario_id = s.loads(token, max_age=1800)['usuario_id'] # 1800s = 30min
        except:
            return None
        return Usuario.query.get(usuario_id)

class Alerta(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data_hora = database.Column(database.DateTime, nullable=False, default=datetime.now)
    imagem_path = database.Column(database.String(255), nullable=False)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)