const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
let obj = {'parking': 'A','time': '2023-03-06 15:11:39','places': Array(18).fill({'etat': ''})};

function display() {
	//ctx.clearRect(0, 0, canvas.width, canvas.height); // clear the canvas
	// Définir la taille et la position des rectangles
	const rect_width = canvas.width / 10;
	const rect_height = canvas.height / 3;
	let rect_x = canvas.width - rect_width;
	let rect_y = canvas.height - rect_height;

	// Dessiner les cadres des rectangles blancs et numéroter les places
	ctx.font = canvas.width / 20 + "px sans-serif";
	ctx.textAlign = "center";
	ctx.textBaseline = "middle";
	for (let i = 0; i < obj.places.length; i++) { // remplacer 18 par le nombre de parkings/liste
		if (obj.places[i].etat == "libre") {
			ctx.fillStyle = "rgb(0, 255, 0)";
		} else {
			ctx.fillStyle = "rgb(255, 0, 0)";
		}
		ctx.fillRect(rect_x, rect_y, rect_width, rect_height);

		const place_num = (i + 1).toString();
		ctx.fillStyle = "rgb(255, 255, 255)";
		ctx.fillText(place_num, rect_x + rect_width / 2, rect_y + rect_height / 2);

		if (i + 1 >= obj.places.length/2) {
			rect_x += rect_width + rect_width / 8;
		} else {
			rect_x -= rect_width + rect_width / 8;
		}
		if (i + 1 == obj.places.length/2) {
			rect_x = 0;
			rect_y = 0;
		}
	}
}
display();
function updatePage() {
  fetch('/content')
    .then(response => response.json())
    .then(data => {
      // Mettre à jour le contenu de la page avec les données reçues du serveur
      obj = Object.assign({}, data);
	  //obj = JSON.parse(data);
      // Redessiner la page avec les nouvelles données
      display();
    });
}

setInterval(updatePage, 2000); // Mettre à jour la page toutes les 2 secondes