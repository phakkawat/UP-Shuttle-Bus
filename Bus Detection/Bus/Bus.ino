// Include Libary.
#include <nRF24L01.h>
#include <printf.h>
#include <RF24.h>
#include <RF24_config.h>
#include <SPI.h>

// Set NRFname and CE,CSN pin Name(CE, CSN).
RF24 radio(8, 7);
// Set NFR beginning node.
byte addresses[][6] = {"0Node", "1Node"};
// Creat integer value.
int Station, BusNumRe, Pass, Count, WaitTime, CH = 0;
int SendPKY = 1, SendCE = 1, SendSCI = 1, SendEN = 1, SendICT = 1;

int BusNum = 2;      // Bus Number

// Function of data sending.
void SendNum(int CH)
{
  radio.setChannel(CH);
  do
  {
    for (Count = 0; Count <= 1; Count++ )
    {
      radio.stopListening();
      radio.write(&BusNum, sizeof(BusNum));
      Serial.print("Send : ");
      Serial.print(BusNum);
      Serial.print("  ");
      delay(200);
      radio.startListening();

      delay(500);

      for (WaitTime = 0 ; WaitTime < 3 ; WaitTime++)
      {
        if (radio.available())
        {
          radio.read(&BusNumRe, sizeof(BusNumRe));
          radio.stopListening();
          Serial.print("\nRecieve : ");
          Serial.print(BusNumRe);
          Serial.println("\n");

          if (BusNum != BusNumRe)
          {
            Count = 0;
            WaitTime = 4;
          }
          else
          {
            Pass = 1;
            WaitTime = 4;
          }
        }
        else delay(1000);
      }
      Count = Count + 1;
    }
    WaitTime = 0;
    delay(1000);
  } while (Pass != 1);
  delay(500);
}

// Function of clearing values.
void FuncClear()
{
  Pass = 0;
  BusNumRe = 0;
  Count = 0;
}

void setup()
{
  // Set Serial at 115200 baud.
  Serial.begin(115200);
  // Set NRF write node, read node, Channel, Datarate, Power, Status.
  radio.begin();
  radio.openWritingPipe(addresses[1]); // Tx.
  radio.openReadingPipe(1, addresses[0]); // Rx.
  radio.setChannel(10);
  radio.setDataRate(RF24_250KBPS);
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening();
}

// Function of main loop.
void loop()
{
  for (Station = 0; Station < 4; Station++)
  {
    Serial.println(Station);        // Print station number.
    do
    {
      delay(1000);                  // Set delay before connect to station.
      if (Station == 0)             // Check station number.
      {
        Serial.print("Station : PKY");      // Print station name.
        CH = 120;                    // Set Bus Channel.
        Serial.print(" --- Channel : ");
        Serial.println(CH);
        Serial.print("Send to PKY : ");
        Serial.println(SendPKY);
        SendPKY++;
      }
      else if (Station == 1)        // Check station number.
      {
        Serial.print("Station : CE");       // Print station name.
        CH = 100;                    // Set Bus Channel.
        Serial.print(" --- Channel : ");
        Serial.println(CH);
        Serial.print("Send to CE : ");
        Serial.println(SendCE);
        SendCE++;
      }
      else if (Station == 2)        // Check station number.
      {
        Serial.print("Station : SCI");      // Print station name.
        CH = 80;                    // Set Bus Channel.
        Serial.print(" --- Channel : ");
        Serial.println(CH);
        Serial.print("Send to SCI : ");
        Serial.println(SendSCI);
        SendSCI++;
      }
      else if (Station == 3)        // Check station number.
      {
        if (BusNum % 2 == 0)        // Check Bus number if it's even number do function of EN station.
        {
          Serial.print("Station : EN");     // Print station name.
          CH = 60;                  // Set Bus Channel.
          Serial.print(" --- Channel : ");
          Serial.println(CH);
          Serial.print("Send to EN : ");
          Serial.println(SendEN);
          SendEN++;
        }
        else
        {
          Serial.print("Station : ICT");    // Print station name.
          CH = 40;                  // Set Bus Channel.
          Serial.print(" --- Channel : ");
          Serial.println(CH);
          Serial.print("Send to ICT : ");
          Serial.println(SendICT);
          SendICT++;
        }
      }
      SendNum(CH);                    // Do function of data sending.
      delay(10000);                 // Waiting for next station transmission.
    } while (Pass == 0);
    FuncClear();                    // Clear values.
  }
  BusNum = BusNum+2;
}
