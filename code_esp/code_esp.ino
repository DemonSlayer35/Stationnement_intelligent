#include <DNSServer.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include "ESPAsyncWebServer.h"
#include "FS.h"
#include "SPIFFS.h"
#include <PubSubClient.h>

const char* ssid     = "A113";       /*Remplacer par le SSID de votre réseau*/
const char* password = "sherbrooke"; /*Remplacer par le mot de passe de votre réseau*/

// MQTT Broker
const char *mqtt_broker = "192.168.0.101"; /*Remplacer par l'adresse IP du broker MQTT*/
const char *topic = "parking/A";           /*Remplacer par le topic MQTT*/
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

DNSServer dnsServer;
AsyncWebServer server(80);

String option1 = ""; // string pour stocker la liste JSON des données du parking

// Fonction pour lister les fichiers sur le système de fichiers SPIFFS.
void listDir(fs::FS &fs, const char * dirname, uint8_t levels){
   Serial.printf("Listing directory: %s\r\n", dirname);

   File root = fs.open(dirname);
   if(!root){
      Serial.println("− failed to open directory");
      return;
   }
   if(!root.isDirectory()){
      Serial.println(" − not a directory");
      return;
   }

   File file = root.openNextFile();
   while(file){
      if(file.isDirectory()){
         Serial.print("  DIR : ");
         Serial.println(file.name());
         if(levels){
            listDir(fs, file.name(), levels -1);
         }
      } else {
         Serial.print("  FILE: ");
         Serial.print(file.name());
         Serial.print("\tSIZE: ");
         Serial.println(file.size());
      }
      file = root.openNextFile();
   }
}

// Classe pour gérer les requêtes de type captive portal
class CaptiveRequestHandler : public AsyncWebHandler {
public:
  CaptiveRequestHandler() {}
  virtual ~CaptiveRequestHandler() {}

  bool canHandle(AsyncWebServerRequest *request){
    return true;
  }

  void handleRequest(AsyncWebServerRequest *request) {
    request->send(SPIFFS, "/captive_page.html","text/html", false);
  }
};

// Fonction pour mettre à jour la page Web avec les données du parking
void update(){
  server.on("/content", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/json", option1);
  });
}

// Fonction pour configurer le serveur Web
void setupServer(){
  // Route qui répond à une requête HTTP GET sur la page d'accueil
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
      request->send(SPIFFS, "/captive_page.html","text/html", false); 
      Serial.println("Client Connected");
  });
   
  // Route qui répond à une requête HTTP GET sur le fichier JavaScript
  server.on("/script.js", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/script.js", "text/js");
  });
   
  // Route qui répond à une requête HTTP GET sur le contenu du parking (format JSON)
  server.on("/content", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/json", option1);
  });
}

void setup(){
  Serial.begin(115200);
   
  // Initialisation de SPIFFS (système de fichiers)
  if(!SPIFFS.begin(true)){
    Serial.println("An Error has occurred while mounting SPIFFS");
    return;
  }
  
  //Lister le contenu du système de fichiers SPIFFS
  listDir(SPIFFS, "/", 0);

  // Configuration du mode d'opération de l'ESP32 (WIFI_AP_STA)
  Serial.println("Setting up AP Mode");
  WiFi.mode(WIFI_AP_STA); 
  WiFi.softAP("Parking"); // Configuration du nom de l'AP (point d'accès)
  
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP()); // Affiche l'adresse IP de l'AP
  Serial.println("Setting up Async WebServer");
  setupServer(); // Configuration du serveur web
  
  Serial.println("Starting DNS Server");
  dnsServer.start(53, "*", WiFi.softAPIP()); // Démarrer le serveur DNS
  server.addHandler(new CaptiveRequestHandler()).setFilter(ON_AP_FILTER); //only when requested from AP

  server.begin(); // Démarrer le serveur web
  Serial.println("All Done!");
  
  // Connexion au point d'accès WIFI
  WiFi.begin(ssid, password);
  Serial.println("\n[*] Connecting to WiFi Network");
  while(WiFi.status() != WL_CONNECTED)
  {
      Serial.print(".");
      delay(100);
  }
  Serial.print("\n[+] Connected to WiFi network with local IP : ");
  Serial.println(WiFi.localIP()); // Affiche l'adresse IP de l'ESP

  // Configuration de la connexion au broker MQTT
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  while (!client.connected()) {
      // Génération d'un identifiant unique pour le client MQTT
      String client_id = "esp32-client-";
      client_id += String(WiFi.macAddress());
      Serial.printf("The client %s connects to the mqtt broker\n", client_id.c_str());
     
      // Tentative de connexion au broker MQTT
      if (client.connect(client_id.c_str())) {
          Serial.println("MQTT connected");
          client.setBufferSize(1024);  // change la taille du buffer à 1024 parce que le message JSON est volumineux
          client.subscribe(topic);
      } else {
          Serial.print("failed with state ");
          Serial.print(client.state());
          delay(2000);
      }
  }
}

// Callback appelé lorsque le client MQTT reçoit un message
void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
   
  // On initialise l'option à une chaîne vide
  option1 = "";
  
  // Conversion des données reçues en chaîne de caractères
  for (int i = 0; i < length; i++) {
      option1 += (char)payload[i];
  }
  
  Serial.println(option1);
  Serial.println();
  Serial.println("-----------------------");
  
  // On appelle la fonction update() pour mettre à jour la page Web avec les nouvelles données du parking
  update();
}


void loop(){
  dnsServer.processNextRequest(); // On gère les requêtes DNS
  client.loop(); // On maintient la connexion MQTT active
}
