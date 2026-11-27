// Mantém a abertura nativa do <details> por clique, Enter e Espaço.
document.querySelectorAll('.menu-dropdown').forEach((menu) => {
  const acionador = menu.querySelector('summary');

  document.addEventListener('click', (event) => {
    if (menu.open && !menu.contains(event.target)) {
      menu.open = false;
    }
  });

  menu.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.open) {
      event.preventDefault();
      menu.open = false;
      acionador.focus();
    }
  });

  menu.addEventListener('focusout', (event) => {
    if (!menu.contains(event.relatedTarget)) {
      menu.open = false;
    }
  });

  menu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      menu.open = false;
    });
  });
});
