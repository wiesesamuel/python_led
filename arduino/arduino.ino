#include "SoftPWM.h"

#pragma pack(push, 1)
struct MessageHeader {
  char magic[2];
  char nr;
  char cmd;
  char data_len;
  char data[0];
};
#pragma pack(pop)

class Pin {
private:
  int nr;
  float brightness = 0.f;
  float frequency = 0.f;
  
public:
  Pin(int nr) {
    this->nr = nr;
  }

  bool receivee(MessageHeader* header) {
    switch (header->cmd) {
      case 0: // set brightness
        if (header->data_len < 1)
          return false;
        this->brightness = header->data[0];
        SoftPWMSetPercent(this->nr, this->brightness);
        return true;
      case 1: // set frequency
        if (header->data_len < 1)
          return false;
        this->frequency = header->data[0];
        return true;
      default:
        return false;
    }
  }
  
  String receive(MessageHeader* header) {
    switch (header->cmd) {
      case 0: // set brightness
        if (header->data_len < 1)
          return "brightness error";
        this->brightness = header->data[0];
        SoftPWMSetPercent(this->nr, this->brightness);
        return "brightness sucess";
      case 1: // set frequency
        if (header->data_len < 1)
          return "frequenz failure";
        this->frequency = header->data[0];
        return "frequenz sucess";
      default:
        return "dafuq u do";
    }
  }
};

// settings
#define BAUD 500000
Pin PIN_LIST[] = {
  Pin(0),
  Pin(1),
  Pin(2),
  Pin(3),
  Pin(4),
  Pin(5),
  Pin(6),
  Pin(7),
  Pin(8),
  Pin(9),
  Pin(10),
  Pin(11),
  Pin(12),
  Pin(13),
  Pin(14),
  Pin(15),
  Pin(16),
  Pin(17),
  Pin(18),
  Pin(19),
  Pin(20),
  Pin(21),
  Pin(22),
  Pin(23),
  Pin(24),
  Pin(25),
};
// state
unsigned char MSG_BUFFER[8];
int MSG_SIZE = 0;

void setup() {
  SoftPWMBegin();
  Serial.begin(BAUD);  
}

void loop() {
  if (Serial.available() > 0) {
    int in = Serial.read();

    // check for buffer overrun
    if (MSG_SIZE >= sizeof(MSG_BUFFER)) {
      MSG_SIZE = 0;
    }

    // save data
    MSG_BUFFER[MSG_SIZE++] = (unsigned char) in;

    // find start
    while (MSG_SIZE >= 2 && (MSG_BUFFER[0] != 0xAA || MSG_BUFFER[1] != 0xAA)) {
      for (int i = 0; i < MSG_SIZE; i++) {
        MSG_BUFFER[i] = MSG_BUFFER[i + 1];
      }
      MSG_SIZE--;
    }

    // check if header arrived
    if (MSG_SIZE >= sizeof(MessageHeader)) {

      // check if data + checksum arrived
      MessageHeader* header = (MessageHeader*) &MSG_BUFFER[0];
      if (header->data_len > sizeof(MSG_BUFFER)) {
        MSG_SIZE = 0;
      } else if (MSG_SIZE >= sizeof(MessageHeader) + header->data_len + 1) {

        unsigned char chk_in = MSG_BUFFER[MSG_SIZE - 1];
        unsigned int chk = 0;
        for (int i = 0; i < MSG_SIZE - 1; i++) {
          chk += MSG_BUFFER[i];
        }

        if ((chk & 0xFF) == (chk_in & 0xFF)) {
          if (header->nr < sizeof(PIN_LIST)) {
            String result = PIN_LIST[header->nr].receive(header);
            Serial.print(result);
            //Serial.write(result ? 1 : 0);
          } else {
            Serial.write(1);
          }
        } else {
            Serial.write(0);
        }
        
        MSG_SIZE = 0;
      }
    }
  }
}
