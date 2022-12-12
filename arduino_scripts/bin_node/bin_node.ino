#include <ESP8266WiFi.h>
#include <Firebase_ESP_Client.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>
#include <NewPing.h>

#define WIFI_SSID "SSID"
#define WIFI_PASSWORD "PASSWORD"
#define API_KEY "API_KEY"
#define DATABASE_URL "URL"
#define DATABASE_SECRETS_TOKEN "TOKEN"
#define TRIGGER_PIN  12
#define ECHO_PIN     11
#define MAX_DISTANCE 200

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

unsigned long previous_millis = 0;
unsigned long update_interval = 60*60*1000;

NewPing distance_sensor(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup()
{
  Serial.begin(115200);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  config.api_key = API_KEY;

  config.database_url = DATABASE_URL;
  config.signer.tokens.legacy_token = DATABASE_SECRETS_TOKEN;

  fbdo.setBSSLBufferSize(2048, 2048);
  fbdo.setResponseSize(2048);

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  Firebase.setDoubleDigits(5);

  config.timeout.serverResponse = 10 * 1000;
}


void loop()
{
  if (Firebase.ready() && (millis() - previous_millis > update_interval || previous_millis == 0))
  {
    int distance = distance_sensor.ping_cm()
    previous_millis = millis();
    Serial.printf("Set state... %s\n", Firebase.RTDB.setInt(&fbdo, F("/103/state"), distance) ? "ok" : fbdo.errorReason().c_str());
  }
}