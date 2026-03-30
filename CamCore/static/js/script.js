const toggle = document.getElementById("menuToggle");
const menu = document.getElementById("menuMobile");

toggle.addEventListener("click", () => {

  menu.classList.toggle("active");

  // Trocar ícone ☰ ↔ X
  if (menu.classList.contains("active")) {
    toggle.textContent = "✕";
  } else {
    toggle.textContent = "☰";
  }

});

const elementos = document.querySelectorAll(
  ".card, .funcoes h2, .subtitulo"
);

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
    }
  });
}, {
  threshold: 0.2
});

elementos.forEach(el => observer.observe(el));


document.addEventListener("DOMContentLoaded", function() {
    const observerOptions = {
        threshold: 0.2 // Dispara quando 20% do elemento estiver visível
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }
        });
    }, observerOptions);

    // Seleciona o texto e a imagem da seção sobre para observar
    const elementosSobre = document.querySelectorAll('.sobre-text, .sobre-image');
    
    elementosSobre.forEach(el => observer.observe(el));
});


//FAQ - Perguntas Frequentes

const perguntas = document.querySelectorAll(".pergunta");

perguntas.forEach(btn => {
  btn.addEventListener("click", () => {

    const item = btn.parentElement;

    item.classList.toggle("ativo");

  });
});

const faqItems = document.querySelectorAll(".faq .item");

const observerFAQ = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
    }
  });
}, {
  threshold: 0.2
});

faqItems.forEach(item => observerFAQ.observe(item));


//Formulário de contato - Enviar mensagem para WhatsApp

function enviarWhats(event) {

  event.preventDefault()

  const nome = document.getElementById('nome').value;
  const mensagem = document.getElementById('mensagem').value;
  const telefone = '5511971017655'

  const texto = `Olá! Me chamo ${nome}, ${mensagem}`
  const msgFormatado = encodeURIComponent(texto)
  const url = `https://wa.me/${telefone}?text=${msgFormatado}`

  window.open(url, '_blank')
}


//FORMULÁRIO ANIMAÇAO

window.addEventListener("load", () => {

  const elementos = document.querySelectorAll(
    ".contato-texto, .contato-form"
  );

  elementos.forEach(el => {
    el.style.opacity = "0";
    el.style.transform = "translateY(80px)";
    el.style.transition = "all 0.8s ease";
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {

        setTimeout(() => {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
        }, index * 150); // efeito em cascata

      }
    });
  }, { threshold: 0.25 });

  elementos.forEach(el => observer.observe(el));

});

