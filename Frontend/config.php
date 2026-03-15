<?php
 $dbHost = 'localhost';
 $dbUsername = 'root';
 $dbPassword = '';
 $dbName = 'users';

 $conexao = new mysqli($dbHost, $dbUsername, $dbPassword, $dbName);

    //Teste de conexão com banco
// if($conexao->connect_errno)
//    {
//        echo 'Erro';
//    }
//    else{
//        echo "Conexão efetuada com sucesso";
//    }
//
//?>