<?php
    if(isset($_POST['submit']))
    {

        include_once('config.php');

        $nome = $_POST['nome'];
        $email = $_POST['email'];
        $senha = $_POST['password'];

        $senhaHash = password_hash($senha, PASSWORD_DEFAULT);

        $result = mysqli_query($conexao, "INSERT INTO usuarios(nome,email,senha) 
        VALUES ('$nome', '$email', '$senhaHash')");


        header('Location: login.php');
        exit();
    }

?>


<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CamCore - Login</title>
    <link rel="stylesheet" href="style.css">
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
            <a href="/Frontend/login.php">
                <button class="btn-nav">Login</button>
            </a>
            <a href="/Frontend/cadastro.php">
                <button class="btn-nav">Cadastro</button>
            </a>
            </div>
    </header>

    <main>
        <form class="login-card" action="cadastro.php" method="POST">
            <h2>Cadastro</h2>


            <div class="form-group">
                <div class="icon">
                    <svg viewBox="0 0 24 24">
                        <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                    </svg>
                </div>
                <input type="text" name="nome" class="input-field" placeholder="Nome" required>
            </div>

            
            <div class="form-group">
                <div class="icon"></div>
                <input type="email" name="email" class="input-field" placeholder="Email" required>
            </div>

            <div class="form-group">
                <div class="icon">
                    <svg viewBox="0 0 24 24">
                        <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM9 6c0-1.66 1.34-3 3-3s3 1.34 3 3v2H9V6zm9 14H6V10h12v10zm-6-3c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z"/>
                    </svg>
                </div>
                <input type="password" name="password" class="input-field" placeholder="Senha" required>
            </div>


            <button type="submit" name='submit' class="btn-submit">Cadastrar</button>
        </form>
    </main>

</body>
</html>