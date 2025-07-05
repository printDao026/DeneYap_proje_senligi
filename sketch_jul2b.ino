#include <WiFi.h> 

const char* ssid = "Modem adı";
const char* password = "modem şifresi";


WiFiServer server(1234);

void setup() {
  pinMode(D0,OUTPUT);
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  server.begin();
  Serial.println("Bağlanılıyor...");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Bağlanıyor");
  }

  Serial.println("Bağlandı");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Yeni istemci baglandi.");

    while (client.connected()) {
      if (client.available()) {
        String data = client.readStringUntil('\n');
        Serial.print("Gelen veri: ");
        Serial.println(data);

        if (data.indexOf("YAK") >= 0) {
          digitalWrite(D0, HIGH);
          Serial.println("LED YAK");

        }

        if (data.indexOf("SONDUR") >= 0) {
          digitalWrite(D0, LOW);
          Serial.println("LED SONDUR");
        }

      }
    }

    client.stop();
    Serial.println("Istemci baglantisi sonlandirildi.");
  }
}
