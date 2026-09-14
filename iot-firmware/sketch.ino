// Codigo ESP32 — PetCare 360 IoT Wearable
// Simulado no Wokwi: https://wokwi.com
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
const char* SSID = "Wokwi-GUEST";
const char* PASSWORD = "";
const char* MQTT_SERVER = "broker.hivemq.com";
const int MQTT_PORT = 1883;
const char* TOPIC = "petcare360/telemetria";
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define LED_R 25
#define LED_G 26
#define LED_B 27
DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient espClient;
PubSubClient client(espClient);
void setup() {
Serial.begin(115200);
dht.begin();
pinMode(LED_R, OUTPUT);
pinMode(LED_G, OUTPUT);
pinMode(LED_B, OUTPUT);
WiFi.begin(SSID, PASSWORD);
while (WiFi.status() != WL_CONNECTED) { delay(500); }
Serial.println("WiFi conectado!");
client.setServer(MQTT_SERVER, MQTT_PORT);
}
void loop() {
if (!client.connected()) { client.connect("petcare360-esp32"); }
client.loop();
float temp = dht.readTemperature();
float umid = dht.readHumidity();
if (!isnan(temp) && !isnan(umid)) {
StaticJsonDocument<200> doc;
doc["pet_id"] = 1;
doc["temperatura"] = temp;
doc["umidade"] = umid;
doc["timestamp"] = millis();
if (temp > 39.5) {
doc["status"] = "ALERTA_FEBRE";
digitalWrite(LED_R, HIGH); digitalWrite(LED_G, LOW);
digitalWrite(LED_B, LOW);
} else if (temp < 37.5) {
doc["status"] = "ALERTA_HIPOTERMIA";
digitalWrite(LED_R, LOW); digitalWrite(LED_G, LOW);
digitalWrite(LED_B, HIGH);
} else {
doc["status"] = "NORMAL";
digitalWrite(LED_R, LOW); digitalWrite(LED_G, HIGH);
digitalWrite(LED_B, LOW);
}
char payload[200];
serializeJson(doc, payload);
client.publish(TOPIC, payload);
Serial.println("Enviado: " + String(payload));
}
delay(5000);
}
