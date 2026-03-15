<?php
  
  session_start();
  if(isset($_POST['submit']))
    {

        include_once('config.php');
        $email = $_POST['email'];
        $senha = $_POST['password'];

        $sql = "SELECT * FROM usuarios WHERE email='$email'";
        $result = $conexao->query($sql);

        


        if($result->num_rows < 1)
        {   
            unset($_SESSION['email']);
            unset($_SESSION['password']);
            header('Location: cadastro.php');
        }
        else
        {

            $user = $result ->fetch_assoc();
            
            if($user && password_verify($senha, $user['senha'])){
                $_SESSION['email'] = $email;
                $_SESSION['password'] = $senha;
                header('Location: sistema.php');
            }
            else{
                header('Location: login.php');    
            
        }
        }

    }
    else
    {   //não acessa
        header('Location: login.php');    
    }
?>