// Récupère le rectangle "Mon profil"
let monProfilRectangle = document.querySelector('.rectangle-interieur:nth-child(1)');

// Récupère le titre et le logo "+"
let monProfilTitre = document.querySelector('.rectangle-interieur:nth-child(1) .titre');
let monProfilLogo = document.querySelector('.rectangle-interieur:nth-child(1) .logo');

// Ajoute un gestionnaire d'événement pour le clic sur le titre
monProfilTitre.addEventListener('click', function() {
  monProfilRectangle.classList.toggle('agrandir');
});

// Ajoute un gestionnaire d'événement pour le clic sur le logo "+"
monProfilLogo.addEventListener('click', function() {
  monProfilRectangle.classList.toggle('agrandir');
});
