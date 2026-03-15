<?php
session_start();

// Limpa todas as variáveis de sessão e destrói a sessão
session_unset();
session_destroy();

header('Location: login.php');
exit();
?>