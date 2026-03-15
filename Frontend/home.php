<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        /* Variáveis de Cores (baseadas na imagem) */
        :root {
            --bg-dark: #121721;        /* Fundo principal escuro */
            --bg-card: #475569;        /* Fundo azul acinzentado (Header e Card) */
            --bg-button: #1a202c;      /* Fundo dos botões (escuro) */
            --bg-input: #94a3b8;       /* Fundo dos inputs (cinza) */
            --text-light: #ffffff;     /* Texto branco */
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-light);
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

                /* === CABEÇALHO (HEADER) === */
        header {
            background-color: var(--bg-card);
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo-container {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 24px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }

        /* SVG simples de uma câmera para simular a logo */
        .logo-icon svg {
            width: 35px;
            height: 35px;
            fill: #cfd6df;
        }

        .nav-buttons {
            display: flex;
            gap: 15px;
        }

        .btn-nav {
            background-color: var(--bg-button);
            color: var(--text-light);
            border: none;
            padding: 10px 25px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.2s;
        }

        .btn-nav:hover {
            opacity: 0.8;
        }

        /* === ÁREA PRINCIPAL E CARD DE LOGIN === */

        
    </style>
</head>
<body>
    <header>
        <div class="logo-container">
            <div class="logo-icon">
                <svg viewBox="0 0 24 24">
                    <path d="M12 15.5c-1.93 0-3.5-1.57-3.5-3.5s1.57-3.5 3.5-3.5 3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5zm7.43-11.19L18.06 2H5.94L4.57 4.31C4.21 4.88 3.61 5.25 2.94 5.25H2C.9 5.25 0 6.15 0 7.25v12.5C0 20.85.9 21.75 2 21.75h20c1.1 0 2-.9 2-2v-12.5c0-1.1-.9-2-2-2h-.94c-.67 0-1.27-.37-1.63-.94zM12 17.5c-3.04 0-5.5-2.46-5.5-5.5s2.46-5.5 5.5-5.5 5.5 2.46 5.5 5.5-2.46 5.5-5.5 5.5z"/>
                </svg>
            </div>
            <span>CamCore</span>
        </div>
            <div class="nav-buttons">
                <button class="btn-nav">Sair</button>
            </a>
            </div>
    </header>
    
</body>
</html>