# CamCore - Sistema de Monitoramento de EPI com visão computacional.
O **CamCore** é um sistema web desenvolvido para aumentar a segurança em ambientes industriais e de construção. Utilizando Visão Computacional e Inteligência Artificial, o sistema monitora em tempo real, através de webcams, se os funcionários estão utilizando o equipamento de proteção individual (Capacete de Segurança). Quando alguém fica 3 segundossem capacete, o sistema dispara um alerta, salva uma foto e registra no banco de dados.

## 🎯 Objetivo do Projeto
Identificar automaticamente o descumprimento das normas de segurança. O sistema funciona com a seguinte lógica:
1. Analisa o frame da câmera em tempo real.
2. Se detectar um funcionário sem capacete, inicia uma contagem de tolerância.
3. Se a violação persistir por **3 segundos**, o sistema emite um alerta visual na tela, captura uma foto do momento exato e registra a infração no banco de dados com data e hora.

## ✨ Funcionalidades
* **Autenticação e Segurança:** Sistema completo de Login, Cadastro e Recuperação de Senha por e-mail para os gestores.
* **Detecção em Tempo Real:** IA rodando no backend que analisa as imagens enviadas diretamente pelo navegador do usuário.
* **Alertas Visuais:** Interface dinâmica que muda de cor (Verde para seguro, Laranja para advertência/contagem, Vermelho para violação registrada).
* **Painel de Relatórios:** Dashboard interativo para consultar o histórico de violações (fotos e horários) com filtros de visualização por Dia, Semana e Mês.
* **Privacidade de Dados:** Os relatórios são isolados por conta/empresa cadastrada no sistema.

## 🛠️ Tecnologias Utilizadas
Este projeto unifica ferramentas modernas de Desenvolvimento Web e Inteligência Artificial:

**Backend:**
* Python
* Flask
* Flask-SQLAlchemy (ORM) & SQLite (Banco de Dados)
* Flask-Login & Flask-Bcrypt (Gestão de Sessão e Criptografia)

**Inteligência Artificial (Visão Computacional):**
* [YOLOv8 (Ultralytics)](https://github.com/ultralytics/ultralytics) para detecção de objetos.
* OpenCV (`cv2`) para processamento das imagens e captura de frames.

**Frontend:**
* HTML5, CSS3 e JavaScript Vanilla.
* Fetch API para comunicação assíncrona (sem recarregar a página) com o backend.
* Jinja2 (Motor de templates do Flask).



## ✒️ Autores
* Alini da Silva - Desenvolvimento Full Stack ---
* Livia Marques - Desenvolvimento Front End e Integração da IA ---
* Maria Eduarda - Desenvolvimento Back end, responsavel pelo Treinamento do Modelo YOLOv8 e Visão Computacional. ---

**Projeto desenvolvido para fins acadêmicos.**
