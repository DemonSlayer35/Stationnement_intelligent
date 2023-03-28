#include <DNSServer.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include "ESPAsyncWebServer.h"
#include "FS.h"
#include "SPIFFS.h"
#include <PubSubClient.h>

const char* ssid     = "A113";   /*Replace with Your own network SSID*/
const char* password = "sherbrooke"; /*Replace with Your own network*/

// MQTT Broker
const char *mqtt_broker = "192.168.0.101";
const char *topic = "parking/A";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

DNSServer dnsServer;
AsyncWebServer server(80);

//String option1 = "{\"parking\": \"A\", \"time\": \"2023-03-06 16:50:08\", \"places\": [{\"id\": 1, \"etat\": \"occupe\"}, {\"id\": 2, \"etat\": \"occupe\"}, {\"id\": 3, \"etat\": \"occupe\"}, {\"id\": 4, \"etat\": \"occupe\"}, {\"id\": 5, \"etat\": \"occupe\"}, {\"id\": 6, \"etat\": \"occupe\"}, {\"id\": 7, \"etat\": \"occupe\"}, {\"id\": 8, \"etat\": \"occupe\"}, {\"id\": 9, \"etat\": \"occupe\"}, {\"id\": 10, \"etat\": \"occupe\"}, {\"id\": 11, \"etat\": \"occupe\"}, {\"id\": 12, \"etat\": \"occupe\"}, {\"id\": 13, \"etat\": \"occupe\"}, {\"id\": 14, \"etat\": \"occupe\"}, {\"id\": 15, \"etat\": \"occupe\"}, {\"id\": 16, \"etat\": \"libre\"}, {\"id\": 17, \"etat\": \"occupe\"}, {\"id\": 18, \"etat\": \"occupe\"}]}";
String option1 = "";

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

class CaptiveRequestHandler : public AsyncWebHandler {
public:
  CaptiveRequestHandler() {}
  virtual ~CaptiveRequestHandler() {}

  bool canHandle(AsyncWebServerRequest *request){
    //request->addInterestingHeader("ANY");
    return true;
  }

  void handleRequest(AsyncWebServerRequest *request) {
    request->send(SPIFFS, "/captive_page.html","text/html", false);
  }
};

void update(){
  server.on("/content", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/json", option1);
  });
}

void setupServer(){
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
      request->send(SPIFFS, "/captive_page.html","text/html", false); 
      Serial.println("Client Connected");
  });

  server.on("/script.js", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/script.js", "text/js");
  });

  server.on("/content", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/json", option1);
  });
}

void setup(){
  Serial.begin(115200);
  if(!SPIFFS.begin(true)){
    Serial.println("An Error has occurred while mounting SPIFFS");
    return;
  }
  
  //List contents of SPIFFS
  listDir(SPIFFS, "/", 0);

  Serial.println();
  Serial.println("Setting up AP Mode");
  WiFi.mode(WIFI_AP_STA); 
  WiFi.softAP("Parking");
  
  Serial.print("AP IP address: ");Serial.println(WiFi.softAPIP());
  Serial.println("Setting up Async WebServer");
  setupServer();
  
  Serial.println("Starting DNS Server");
  dnsServer.start(53, "*", WiFi.softAPIP());
  server.addHandler(new CaptiveRequestHandler()).setFilter(ON_AP_FILTER);//only when requested from AP

  server.begin();
  Serial.println("All Done!");

  WiFi.begin(ssid, password);  //Connecting to Defined Access point
  Serial.println("\n[*] Connecting to WiFi Network");
  while(WiFi.status() != WL_CONNECTED)
  {
      Serial.print(".");
      delay(100);
  }
  Serial.print("\n[+] Connected to WiFi network with local IP : ");
  Serial.println(WiFi.localIP());   //Printing IP address of Connected network

  //connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  while (!client.connected()) {
      String client_id = "esp32-client-";
      client_id += String(WiFi.macAddress());
      Serial.printf("The client %s connects to the mqtt broker\n", client_id.c_str());
      if (client.connect(client_id.c_str()))/*, mqtt_username, mqtt_password))*/ {
          Serial.println("MQTT connected");
          client.setBufferSize(1024);
          client.subscribe(topic);
      } else {
          Serial.print("failed with state ");
          Serial.print(client.state());
          delay(2000);
      }
  }
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  option1 = "";
  
  for (int i = 0; i < length; i++) {
      option1 += (char)payload[i];
  }
  
  Serial.println(option1);
  Serial.println();
  Serial.println("-----------------------");
  
  update();
}


void loop(){
  dnsServer.processNextRequest();
  client.loop();
}
