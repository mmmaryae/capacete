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
      
      card.innerHTML = `
        <img src="${alerta.imagem}" alt="Violação de EPI" class="alerta-img">
        <div class="alerta-info">
          <span class="alerta-data">${alerta.data}</span>
          <span class="alerta-hora"> ${alerta.hora}</span>
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