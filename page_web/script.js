const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
let obj = {
  "parking": "A",
  "time": "2023-03-06 15:11:39",
  "places": Array(18).fill({"etat": ""})
};

// Créez un nouveau client MQTT
const client = new Paho.Client("10.240.9.128", 8080, "myclientid_");
const topic = "parking/A";
// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// Fonction pour récupérer la liste depuis l'API REST
async function getListe() {
	console.log("getListe");
    client.connect({ onSuccess: onConnect });
}

function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe(topic);
  //var message = new Paho.Message("Hello");
  //message.destinationName = topic;
  //client.send(message);
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

function onMessageArrived(message) {
  console.log("onMessageArrived:" + message.payloadString);
  obj = JSON.parse(message.payloadString);
  client.disconnect();
}

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

getListe();
display();
setInterval(function () {
    getListe();
    display();
}, 2000);
