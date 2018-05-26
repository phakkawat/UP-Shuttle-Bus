//*********************************************Espresso***************************************************************
#include <ESP8266WiFi.h>
#include <MicroGear.h>

const char* ssid     = "Test";
const char* password = "123456780";

#define APPID   "UPshuttlebus"
#define KEY     "beUIYcyNimrRb40"
#define SECRET  "YuuToXm7FeraLdstDC3Agw3gj"
#define ALIAS   "Station02"
#define TargetWeb "HTMLMonitor02"

WiFiClient client;

int timer = 0, CountSend = 1, OE = 0;

//**************************************************NRF***************************************************************
#include <nRF24L01.h>
#include <RF24.h>
#include <RF24_config.h>
#include <SPI.h>

RF24 radio(15, 2);
byte addresses[][6] = {"0Node", "1Node"};

int BusNum = 0;

void FuncClear()
{
  BusNum = 0;
  timer = 0;
  OE = 0;
}

//**********************************************Espresso***************************************************************
MicroGear microgear(client);

void onMsghandler(char *topic, uint8_t* msg, unsigned int msglen) {
  Serial.print("Incoming message --> ");
  msg[msglen] = '\0';
  Serial.println((char *)msg);
}
void onConnected(char *attribute, uint8_t* msg, unsigned int msglen) {
  Serial.println("Connected to NETPIE...");
  microgear.setAlias(ALIAS);
}

void toNetpie(int BusNum)
{
  radio.write(&BusNum, sizeof(BusNum));
  delay(1000);
  radio.write(&BusNum, sizeof(BusNum));
  Serial.print("Send to Bus : ");
  Serial.println(BusNum);

  String str = "SCI";

  str += ":" + String(BusNum);

  String data;

  OE = BusNum % 2;
  if (OE == 0)
  {
    data = "/" + String(BusNum) + "/E0";
  }
  else
  {
    data = "/" + String(BusNum) + "/O0";
  }

  char msg[256];
  data.toCharArray(msg, data.length());

  if (microgear.connected())
  {
    microgear.connect(APPID);
    Serial.println("connected");
    microgear.loop();
    microgear.writeFeed("UPshuttlebus", str, "69K4sOltXlCxTff9ukvKqJLmmy0iAuXd");      // Send data to feed
    delay(200);
    microgear.chat(TargetWeb, msg);
    Serial.print("Message to Web : ");
    Serial.println(msg);
    Serial.println(str);
    Serial.print("Data is Send : ");
    Serial.println(BusNum);
    delay(1000);
    Serial.print("Mission Success ");
    Serial.println(CountSend);
    Serial.print("\n");
    CountSend++;
  }
  else
  {
    Serial.println("connection lost, reconnect...");
    microgear.connect(APPID);
    if (microgear.connected())
    {
      Serial.println("connected");
      microgear.writeFeed("UPshuttlebus", str, "69K4sOltXlCxTff9ukvKqJLmmy0iAuXd");      // Send data to feed
      delay(200);
      microgear.chat(TargetWeb, msg);
      Serial.print("Message to Web : ");
      Serial.println(msg);
      Serial.println(str);
      Serial.print("Data is Send : ");
      Serial.println(BusNum);
      delay(1000);
      Serial.print("Mission Success ");
      Serial.println(CountSend);
      Serial.print("\n");
      CountSend++;
    }
  }
  delay(100);
}


void setup()
{
  //******************************************************NRF*************************************************************************************
  Serial.begin(115200);
  radio.begin();
  radio.openWritingPipe(addresses[0]);      // (Tx) = radio.openWritingPipe("0Node")
  radio.openReadingPipe(1, addresses[1]);     // Rx
  radio.setChannel(80);
  radio.setDataRate(RF24_250KBPS);
  radio.setPALevel(RF24_PA_MAX);
  radio.stopListening();

  delay(100);

  Serial.println("Ready...");

  //*****************************************************Espresso**********************************************************************************
  microgear.on(MESSAGE, onMsghandler);
  microgear.on(CONNECTED, onConnected);

  Serial.println("Starting...");

  if (WiFi.begin(ssid, password))
  {
    while (WiFi.status() != WL_CONNECTED)
    {
      delay(500);
      Serial.print(".");
    }
  }

  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  microgear.init(KEY, SECRET, ALIAS);

  microgear.connect(APPID);

  Serial.println("Reciever SCI\n");
}



void loop()
{
  for (timer = 0 ; timer < 600 ; timer++)     //Reconnect Wi-Fi every 10 Minutes
  {
    radio.startListening();     // nRF24L01n ready to recieve the value
    if (radio.available())
    {
      radio.read(&BusNum, sizeof(BusNum));    // Recieve bus number from transmission device.
      Serial.print("Recieve : ");
      Serial.print(BusNum);
      Serial.print("  ");

      delay(200);

      radio.stopListening();      // nRF24L01n not ready to recieve the value
      delay(500);

      Serial.println("************Sent Data***************");
      toNetpie(BusNum);     // Send value to NETPIE.
      FuncClear();    // Clear all values.

      delay(15000);
      Serial.println("Ready...");
    }

    if (timer == 180)
    {
      microgear.chat(TargetWeb, "/00");
    }

    delay(1000);
  }

  WiFi.disconnect();      // Disconnect WiFi
  delay(200);

  if (WiFi.begin(ssid, password)) // Reconnect WiFi
  {
    while (WiFi.status() != WL_CONNECTED)
    {
      delay(500);
      Serial.print(".");
    }
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  microgear.init(KEY, SECRET, ALIAS);

  microgear.connect(APPID);   // Connect to NETPIE

  Serial.println("Reciever SCI\n");

  timer = 0;
}
