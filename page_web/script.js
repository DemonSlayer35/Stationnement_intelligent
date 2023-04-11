// Récupérer le canevas et son contexte
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Définir les dimensions du canevas
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Objet qui stocke les informations du parking
let obj = {
  "parking": "A",
  "time": "2023-03-06 15:11:39",
  "places": Array(18).fill({"etat": ""})
};

// Créez un nouveau client MQTT
const client = new Paho.Client("10.240.9.128", 8080, "myclientid_"); // Entrer l'adresse IP du broker MQTT
const topic = "parking/A";					     // Entrer le nom du topic MQTT

// Définir les fonctions de rappel pour la connexion MQTT
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// Fonction pour récupérer la liste depuis le topic MQTT
async function getListe() {
    console.log("getListe");
    client.connect({ onSuccess: onConnect });
}

// Fonction appelée lorsque la connexion est établie
function onConnect() {
  // Une fois la connexion établie, s'abonne au topic
  console.log("onConnect");
  client.subscribe(topic);
}

// Fonction appelée lorsqu'une connexion est perdue
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

// Fonction appelée lorsqu'un message est reçu
function onMessageArrived(message) {
  console.log("onMessageArrived:" + message.payloadString);
  obj = JSON.parse(message.payloadString); // Convertir le message reçu en objet JSON
  client.disconnect(); // Déconnecter le client MQTT
}

// Fonction pour dessiner les places de parking sur le canevas
function display() {
	// Définir la taille et la position des rectangles
	const rect_width = canvas.width / 10; // Largeur du rectangle est 1/10 de la largeur du canevas
	const rect_height = canvas.height / 3; // Hauteur du rectangle est 1/3 de la hauteur du canevas
	let rect_x = canvas.width - rect_width;
	let rect_y = canvas.height - rect_height;

	// Dessiner les cadres des rectangles blancs et numéroter les places
	ctx.font = canvas.width / 20 + "px sans-serif";
	ctx.textAlign = "center"; // Centrer les numéros horizontalement
	ctx.textBaseline = "middle"; // Centrer les numéros verticalement
	for (let i = 0; i < obj.places.length; i++) {
		if (obj.places[i].etat == "libre") {
			ctx.fillStyle = "rgb(0, 255, 0)"; // Si la place est libre, remplir le rectangle en vert
		} else {
			ctx.fillStyle = "rgb(255, 0, 0)"; // Sinon, remplir le rectangle en rouge
		}
		ctx.fillRect(rect_x, rect_y, rect_width, rect_height); // Dessiner le rectangle
		
		// Écrire le numéro de la place au centre du rectangle
		const place_num = (i + 1).toString();
		ctx.fillStyle = "rgb(255, 255, 255)";
		ctx.fillText(place_num, rect_x + rect_width / 2, rect_y + rect_height / 2);
		
		// Si on est dans la deuxième rangée du parking, numéroter vers la droite
		if (i + 1 >= obj.places.length/2) { 
			rect_x += rect_width + rect_width / 8;
		} else { // Sinon, numéroter vers la gauche
			rect_x -= rect_width + rect_width / 8;
		}
		// Si on est à la moitié du nombre de places, passer à la deuxième rangée
		if (i + 1 == obj.places.length/2) {
			rect_x = 0;
			rect_y = 0;
		}
	}
}

getListe(); // Récupérer la liste des places de parking une première fois au chargement de la page
display(); // Dessiner les places de parking une première fois au chargement de la page

// Mettre à jour la liste des places de parking et les dessiner toutes les 2 secondes
setInterval(function () {
    getListe();
    display();
}, 2000);
