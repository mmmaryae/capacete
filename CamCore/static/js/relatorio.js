const botoesFiltro = document.querySelectorAll('.filtro-btn');
const gridAlertas = document.getElementById('gridAlertas');
const totalAlertasText = document.getElementById('total-alertas');

// Função que busca os dados no Flask
async function carregarRelatorio(periodo) {
  // Mostra estado de carregamento
  gridAlertas.innerHTML = '<p style="color: white;">Buscando registros no banco de dados...</p>';
  
  try {
    // Chama a API passando o período escolhido na URL
    const response = await fetch(`/api/alertas?periodo=${periodo}`);
    const data = await response.json();

    // Atualiza o contador de total
    totalAlertasText.innerHTML = `Total de violações registradas: <strong>${data.total}</strong>`;

    gridAlertas.innerHTML = '';

    if (data.total === 0) {
      gridAlertas.innerHTML = '<p class="msg-vazio">Nenhuma violação registrada neste período. Parabéns à equipe!</p>';
      return;
    }

    // Cria um "cartão" para cada alerta recebido
    data.alertas.forEach(alerta => {
      const card = document.createElement('div');
      card.className = 'alerta-card';
      
      // ADIÇÃO 1: Coloquei um ID no card para o JavaScript saber quem apagar depois
      card.id = `card-alerta-${alerta.id}`; 
      
      // ADIÇÃO 2: Adicionei o botão de Excluir dentro do HTML do card
      card.innerHTML = `
        <img src="${alerta.imagem}" alt="Violação de EPI" class="alerta-img">
        <div class="alerta-info">
          <span class="alerta-data">${alerta.data}</span>
          <span class="alerta-hora"> ${alerta.hora}</span>
          <button onclick="deletarAlerta(${alerta.id})" class="btn-deletar-card">
              Excluir
          </button>
        </div>
      `;
      
      gridAlertas.appendChild(card);
    });

  } catch (erro) {
    console.error("Erro ao carregar relatórios:", erro);
    gridAlertas.innerHTML = '<p style="color: red;">Erro ao carregar dados. Verifique o servidor.</p>';
  }
}

// Configura o clique dos botões
botoesFiltro.forEach(botao => {
  botao.addEventListener('click', () => {
    // Remove a classe "active" de todos e coloca só no clicado
    botoesFiltro.forEach(b => b.classList.remove('active'));
    botao.classList.add('active');

    // Pega o valor (hoje, semana, ou mes) e busca no banco
    const periodoSelecionado = botao.getAttribute('data-periodo');
    carregarRelatorio(periodoSelecionado);
  });
});

// Assim que a página abrir, carrega os dados de "Hoje" automaticamente
window.onload = () => {
  carregarRelatorio('hoje');
};


async function deletarAlerta(alertaId) {
  const confirmacao = confirm("Tem certeza que deseja apagar este alerta? A foto será excluída.");
  
  if (!confirmacao) return;

  try {
    const resposta = await fetch(`/api/alertas/${alertaId}`, {
      method: 'DELETE'
    });

    if (resposta.ok) {
      // Pega o card que acabou de ser deletado
      const card = document.getElementById(`card-alerta-${alertaId}`);
      if (card) {
        // Faz uma animação de sumiço bonitinha
        card.style.transition = "all 0.4s ease";
        card.style.opacity = "0";
        card.style.transform = "scale(0.9)";
        
        setTimeout(() => {
          card.remove(); // Remove o HTML definitivamente
          
          // Recarrega a aba atual para atualizar os números lá em cima
          const abaAtiva = document.querySelector('.filtro-btn.active').getAttribute('data-periodo');
          carregarRelatorio(abaAtiva);
          
        }, 400);
      }
    } else {
      const dados = await resposta.json();
      alert("Erro ao deletar: " + (dados.erro || "Falha desconhecida"));
    }

  } catch (erro) {
    console.error("Erro na requisição DELETE:", erro);
    alert("Erro de conexão. Verifique o console.");
  }
}