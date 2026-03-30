from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from CamCore.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confimacao = SubmitField("Fazer login")


class FormResetarSenha(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    botao_confimacao = SubmitField("Resetar senha")

class FormNovaSenha(FlaskForm):
    senha = PasswordField("Nova Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirme a Nova Senha", 
                                     validators=[DataRequired(), EqualTo("senha")])
    botao_confimacao = SubmitField("Alterar Senha")

class FormCriarConta(FlaskForm):
    nome = StringField("Seu nome", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField(
        "Confirmação de Senha",
        validators=[DataRequired(), EqualTo("senha")]
    )
    botao_confimacao = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça login para continuar")