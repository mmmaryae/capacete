const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const statusBox = document.getElementById("status");
const btnCamera = document.getElementById("btnCamera");
const btnText = document.getElementById("btnText");
const cameraBox = document.getElementById("cameraBox");
const alertaViolacao = document.getElementById("alertaViolacao");
const btnOkAlerta = document.getElementById("btnOkAlerta"); // Opcional agora, mas mantido para não quebrar o HTML
const ctx = canvas.getContext("2d");

let cameraAtiva = false;
let streamAtivo = null;
let processando = false;
let ultimoEnvio = 0;
let religando = false;

// Liga e desliga a câmera pelo botão
btnCamera.addEventListener("click", async () => {
  if (!cameraAtiva) {
    await ligarCamera();
  } else {
    desligarCamera();
  }
});

// Fecha o alerta manualmente se o usuário clicar (embora agora feche sozinho)
if(btnOkAlerta) {
    btnOkAlerta.addEventListener("click", () => {
      alertaViolacao.style.display = "none";
      cameraBox.classList.remove("violation");
    });
}

async function ligarCamera() {
  try {
    streamAtivo = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false
    });

    const track = streamAtivo.getVideoTracks()[0];

    if (track) {
      track.onended = async () => {
        console.warn("A TRACK DA CÂMERA FOI ENCERRADA");
        statusBox.textContent = "Câmera encerrada. Tentando religar...";
        statusBox.style.background = "orange";

        if (cameraAtiva && !religando) {
          await tentarReligarCamera();
        }
      };
    }

    video.onpause = () => console.warn("O vídeo foi pausado");
    video.onended = () => console.warn("O vídeo terminou");

    video.srcObject = streamAtivo;
    await video.play();

    cameraAtiva = true;
    processando = false;
    ultimoEnvio = 0;
    religando = false;

    btnText.textContent = "Desligar Câmera";
    btnCamera.classList.add("active");
    statusBox.textContent = "Câmera ligada. Iniciando monitoramento...";
    statusBox.style.background = "green";

    loop();
  } catch (err) {
    console.error("Erro ao acessar câmera:", err);
    statusBox.textContent = "Erro ao acessar câmera";
    statusBox.style.background = "orange";
  }
}

async function tentarReligarCamera() {
  religando = true;
  try {
    if (streamAtivo) {
      streamAtivo.getTracks().forEach(track => track.stop());
    }

    streamAtivo = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false
    });

    const track = streamAtivo.getVideoTracks()[0];

    if (track) {
      track.onended = async () => {
        console.warn("A TRACK DA CÂMERA FOI ENCERRADA DE NOVO");
        statusBox.textContent = "Câmera encerrada. Tentando religar...";
        statusBox.style.background = "orange";

        if (cameraAtiva && !religando) {
          await tentarReligarCamera();
        }
      };
    }

    video.srcObject = streamAtivo;
    await video.play();

    statusBox.textContent = "Câmera religada";
    statusBox.style.background = "green";
  } catch (err) {
    console.error("Erro ao religar câmera:", err);
    statusBox.textContent = "Erro ao religar câmera";
    statusBox.style.background = "red";
  } finally {
    religando = false;
  }
}

function desligarCamera() {
  cameraAtiva = false;
  processando = false;
  religando = false;

  if (streamAtivo) {
    streamAtivo.getTracks().forEach(track => track.stop());
    streamAtivo = null;
  }

  video.pause();
  video.srcObject = null;

  btnText.textContent = "Ligar Câmera";
  btnCamera.classList.remove("active");
  statusBox.textContent = "Câmera desligada";
  statusBox.style.background = "rgba(0,0,0,0.6)";
  
  // Limpa todos os alertas visuais
  alertaViolacao.style.display = "none";
  cameraBox.classList.remove("violation", "warning");
}

function loop() {
  if (!cameraAtiva) return;

  requestAnimationFrame(loop);

  const agora = Date.now();
  // Envia a foto a cada 700ms (quase 1 segundo)
  if (agora - ultimoEnvio < 700 || processando || video.readyState !== 4) return;

  ultimoEnvio = agora;
  enviarFrame();
}

async function enviarFrame() {
  if (!cameraAtiva || !streamAtivo) return;

  processando = true;

  try {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    if (!canvas.width || !canvas.height) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const blob = await new Promise(resolve => {
      canvas.toBlob(resolve, "image/jpeg", 0.8);
    });

    if (!blob) {
      console.error("Falha ao gerar blob");
      return;
    }

    // 1. CHAMA A NOSSA NOVA ROTA NO FLASK
    const response = await fetch("/api/processar", {
      method: "POST",
      body: blob
    });

    const data = await response.json();

    // 2. LÓGICA VISUAL BASEADA NA RESPOSTA DA IA
    if (data.status === "sem_capacete") {
      
      if (data.alerta) {
        // Passou dos 10 segundos! Tira a foto e dá o alerta máximo.
        cameraBox.classList.remove("warning");
        cameraBox.classList.add("violation");
        alertaViolacao.style.display = "flex";
        statusBox.style.background = "red";
        statusBox.textContent = "ALERTA: Violação Registrada no Banco!";

        // Faz o alerta sumir sozinho depois de 3 segundos
        setTimeout(() => {
          alertaViolacao.style.display = "none";
          cameraBox.classList.remove("violation");
        }, 3000);

      } else {
        // Sem capacete, mas ainda contando o cronômetro
        cameraBox.classList.remove("violation");
        cameraBox.classList.add("warning"); 
        alertaViolacao.style.display = "none";
        statusBox.style.background = "orange";
        statusBox.textContent = `Atenção: Sem capacete! Tempo: ${data.tempo}s`;
      }

    } else {
      // Com capacete (Seguro)
      cameraBox.classList.remove("violation", "warning");
      alertaViolacao.style.display = "none";
      statusBox.style.background = "green"; 
      statusBox.textContent = "Monitorando: Com capacete";
    }

  } catch (err) {
    console.error("Erro na API:", err);
    statusBox.textContent = "Erro ao processar imagem. Verifique o servidor.";
    statusBox.style.background = "orange";
  } finally {
    processando = false;
  }
}