const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const screen_width = 1152;
const screen_height = 648;
liste = [];

// Fonction pour récupérer la liste depuis l'API REST
async function getListe() {
    const response = await fetch('http://10.0.0.98:5000/moyenne'); //mettre l'adresse du serveur flask
    const data = await response.json();
    liste = JSON.parse(data);

    /*// Accès à chaque élément de la liste
    for (let i = 0; i < liste.length; i++) {
      console.log(liste[i]);
    }*/
}

function display() {
  // Remplir l'écran avec du noir
  ctx.fillStyle = "rgb(0, 0, 0)";
  ctx.fillRect(0, 0, screen_width, screen_height);

  // Définir la taille et la position des rectangles
  const rect_width = screen_width / 10;
  const rect_height = screen_height / 3;
  let rect_x = screen_width - rect_width - 37;
  let rect_y = rect_height + rect_height / 2 + 54;

  // Dessiner les cadres des rectangles blancs et numéroter les places
  ctx.font = "36px sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  for (let i = 0; i < 18; i++) {
    if (liste[i] < 1) {
      ctx.fillStyle = "rgb(0, 255, 0)";
    } else {
      ctx.fillStyle = "rgb(255, 0, 0)";
    }
    ctx.fillRect(rect_x, rect_y, rect_width, rect_height);

    const place_num = (i + 1).toString();
    ctx.fillStyle = "rgb(255, 255, 255)";
    ctx.fillText(place_num, rect_x + rect_width / 2, rect_y + rect_height / 2);

    if (i + 1 >= 9) {
      rect_x += rect_width + 5;
    } else {
      rect_x -= rect_width + 5;
    }
    if (i === 8) {
      rect_x = 37;
      rect_y = 54;
    }
  }
}
setInterval(function () {
    getListe();
    display();
}, 5000);
