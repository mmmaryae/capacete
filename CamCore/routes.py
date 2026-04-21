import os
import time
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime, date,  timedelta
from flask import render_template, url_for, redirect, request, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from flask_mail import Message # <-- Adicionado para montar o e-mail

# Importações do seu projeto
from CamCore import app, database, bcrypt, mail
from CamCore.forms import FormCriarConta, FormLogin, FormResetarSenha, FormNovaSenha
from CamCore.models import Usuario, Alerta


# ==============================================================================
# CONFIGURAÇÕES DA IA (YOLO)
# ==============================================================================
BASE_DIR = Path(__file__).parent.parent
MODEL_PATH = BASE_DIR / "model" / "best.pt"
CAPTURE_DIR = BASE_DIR / "CamCore" / "static" / "captures"
CAPTURE_DIR.mkdir(parents=True, exist_ok=True)

# Carrega o modelo apenas uma vez quando o servidor inicia
model = YOLO(str(MODEL_PATH))

# Dicionário para controlar o tempo de cada usuário sem capacete
estados_usuarios = {}

def get_estado_usuario(usuario_id):
    if usuario_id not in estados_usuarios:
        estados_usuarios[usuario_id] = {
            "tempo_sem_capacete_inicio": None,
            "ultimo_alerta": 0
        }
    return estados_usuarios[usuario_id]

# ==============================================================================
# ROTAS ORIGINAIS (FRONTEND E LOGIN)
# ==============================================================================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        # O generate_password_hash no Flask-Bcrypt mais recente requer o .decode('utf-8') para salvar como string no banco
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(nome=form_criarconta.nome.data,
                          senha=senha_cript, email=form_criarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("sistema"))
    return render_template("cadastro.html", form=form_criarconta)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)
            return redirect(url_for("sistema"))
        else:
            flash('E-mail ou senha incorretos. Tente novamente.', 'danger')
    return render_template("login.html", form=form)


@app.route("/perfil/<int:usuario_id>")
@login_required
def perfil(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    return render_template("perfil.html", usuario_id=usuario.id)


@app.route("/camera")
@login_required
def sistema():
    return render_template("camera.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))




# ==============================================================================
# LÓGICA DE RECUPERAÇÃO DE SENHA
# ==============================================================================

def send_mail(usuario):
    token = usuario.get_token_reset()
    # O remetente no Mailtrap pode ser qualquer um
    msg = Message('Redefinição de Senha - CamCore',
                  sender='noreply@camcore.com', 
                  recipients=[usuario.email])
    
    link = url_for('mudar_senha', token=token, _external=True)
    
    # O link sempre vai aparecer no terminal
    print(f"\n--- LINK DE RESET (Cópia de Segurança) ---\n{link}\n------------------------------------------\n")
    
    try:
        mail.send(msg)
        print("Sucesso: O e-mail chegou no Mailtrap!")
    except Exception as e:
        # Se der erro de rede, o sistema não trava a tela do usuário
        print(f"Erro de conexão com o Mailtrap: {e}")

@app.route("/reset_senha", methods=['GET', 'POST'])
def reset_senha():
    """Rota que mostra o formulário para pedir o reset de senha"""
    form = FormResetarSenha()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario:
            send_mail(usuario)
            # Mostra mensagem verde de sucesso no login
            flash('Um e-mail foi enviado com instruções para redefinir sua senha.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Não encontramos uma conta com este e-mail. Faça o cadastro.', 'danger')
            
    return render_template('reset_senha.html', title='Modificar Senha', form=form)


@app.route("/reset_senha/<token>", methods=['GET', 'POST'])
def mudar_senha(token):
    """Rota que o usuário acessa ao clicar no link do e-mail"""
    # Verifica se o token é válido e retorna o usuário dono dele
    usuario = Usuario.verificar_token_reset(token)
    
    if not usuario:
        flash('O link de redefinição é inválido ou expirou.', 'danger')
        return redirect(url_for('reset_senha'))
    
    # Mostra o formulário para digitar a senha nova
    form = FormNovaSenha()
    if form.validate_on_submit():
        # Criptografa a senha nova e salva no banco de dados
        nova_senha_cript = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario.senha = nova_senha_cript
        database.session.commit()
        
        flash('Sua senha foi atualizada com sucesso! Você já pode fazer login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('mudar_senha.html', title='Nova Senha', form=form)




# ==============================================================================
# ROTAS DA IA E RELATÓRIOS
# ==============================================================================

@app.route("/api/processar", methods=["POST"])
@login_required
def processar_frame():
    usuario_id = current_user.id
    
    # 1. Recebe a imagem da câmera
    body = request.data
    nparr = np.frombuffer(body, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"erro": "Frame inválido"}), 400

    # 2. Roda a IA
    results = model(frame, verbose=False)
    detectou_sem_capacete = any(
        model.names[int(box.cls[0].item())] == "sem_capacete"
        for box in (results[0].boxes or [])
    )

    estado = get_estado_usuario(usuario_id)
    agora = time.time()
    alerta_gerado = False

    # 3. Lógica de Negócio (10 segundos)
    if detectou_sem_capacete:
        if estado["tempo_sem_capacete_inicio"] is None:
            estado["tempo_sem_capacete_inicio"] = agora
        
        tempo_decorrido = agora - estado["tempo_sem_capacete_inicio"]

        # Se passou de 10 segundos sem capacete e não está em cooldown
        if tempo_decorrido >= 10 and (agora - estado["ultimo_alerta"]) >= 10:
            # Salva a imagem
            nome_arquivo = f"alerta_{usuario_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            caminho_salvamento = CAPTURE_DIR / nome_arquivo
            cv2.imwrite(str(caminho_salvamento), frame)

            # Registra no Banco de Dados
            novo_alerta = Alerta(
                data_hora=datetime.now(),
                imagem_path=f"captures/{nome_arquivo}", # Salva caminho relativo
                usuario_id=usuario_id
            )
            database.session.add(novo_alerta)
            database.session.commit()

            # Reseta os cronômetros
            estado["ultimo_alerta"] = agora
            estado["tempo_sem_capacete_inicio"] = None
            alerta_gerado = True
            
        status = "sem_capacete"
    else:
        # Se colocou o capacete, zera o cronômetro
        estado["tempo_sem_capacete_inicio"] = None
        status = "com_capacete"
        tempo_decorrido = 0

    return jsonify({
        "status": status,
        "tempo": round(tempo_decorrido, 1),
        "alerta": alerta_gerado
    })

@app.route("/api/alertas", methods=["GET"])
@login_required
def buscar_alertas():
    periodo = request.args.get('periodo', 'hoje') # Pega a palavra que o JS mandou
    hoje = date.today()
    
    # Define a data limite baseada no filtro escolhido
    if periodo == 'semana':
        data_limite = hoje - timedelta(days=7)
    elif periodo == 'mes':
        data_limite = hoje - timedelta(days=30)
    else:
        # Padrão: Hoje
        data_limite = hoje

    # Faz a consulta no banco: Alertas do usuário atual DEPOIS da data limite
    alertas = Alerta.query.filter(
        Alerta.usuario_id == current_user.id,
        database.func.date(Alerta.data_hora) >= data_limite
    ).order_by(Alerta.data_hora.desc()).all()
    
    lista_alertas = []
    for a in alertas:
        lista_alertas.append({
            "id": a.id,
            "data": a.data_hora.strftime("%d/%m/%Y"), # Formata a data (Ex: 25/10/2023)
            "hora": a.data_hora.strftime("%H:%M:%S"), # Formata a hora (Ex: 14:30:00)
            "imagem": url_for('static', filename=a.imagem_path)
        })

    return jsonify({"total": len(lista_alertas), "alertas": lista_alertas})

# Rota para renderizar a página HTML
@app.route("/relatorios")
@login_required
def relatorios_page():
    return render_template("relatorios.html")


# ==============================================================================
#  RELATÓRIOS
# ==============================================================================
@app.route("/relatorio", methods=["GET"])
def relatorio():
    return render_template("relatorio.html")