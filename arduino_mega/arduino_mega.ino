 #include "SoftPWM.h"
#include <EEPROM.h>

#pragma pack(push, 1)
struct MessageHeader {
  char magic[2];
  char nr;
  char cmd;
  char data_len;
  char data[0];
};
#pragma pack(pop)

static size_t PWM_PINS[] = {
  13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2,
  44, 46, 45,
};

class Pin {
private:
  int nr;
  int brightness = 0;
  float frequency = 0.f;
  bool pwm = false;
  
public:
  Pin(int nr) {
    this->nr = nr;
    for (auto &pwm : PWM_PINS) {
      if (this->nr == pwm) {
        pinMode(this->nr, OUTPUT);
        this->pwm = true;
        break;
      }
    }
  }

  bool receive(MessageHeader* header) {
    switch (header->cmd) {
      case 0: // set brightness
        if (header->data_len < 1)
          return false;
        this->brightness = header->data[0];
        if (this->pwm) {
          analogWrite(this->nr, this->brightness);
        } else {
          SoftPWMSet(this->nr, this->brightness);
        }
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
};

// settings
#define BAUD 500000
#define EEPROM_SIZE 8
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
  Pin(26),
  Pin(27),
  Pin(28),
  Pin(29),
  Pin(30),
  Pin(31),
  Pin(32),
  Pin(33),
  Pin(34),
  Pin(35),
  Pin(36),
  Pin(37),
  Pin(38),
  Pin(39),
  Pin(40),
  Pin(41),
  Pin(42),
  Pin(43),
  Pin(44),
  Pin(45),
  Pin(46),
  Pin(47),
  Pin(48),
  Pin(49),
  Pin(50),
  Pin(51),
  Pin(52),
  Pin(53),
  Pin(54),
  Pin(55),
};

// state
bool handshake = false;
unsigned char MSG_BUFFER[8];
int MSG_SIZE = 0;
byte id[EEPROM_SIZE];


void setup_id() {
  // get id
  for (int i = 0; i < EEPROM_SIZE; i++) {
    id[i] = EEPROM.read(i);
  }
  
  // check if id is valid
  if (!(id[0] == 0x6C && id[1] == 0x65 && id[2] == 0x64)) {
    EEPROM.write(0, 0x6C);
    EEPROM.write(1, 0x65);
    EEPROM.write(2, 0x64);
    
    id[0] = 0x6C;
    id[2] = 0x65;
    id[3] = 0x64;
    
    for (int i = 3; i < EEPROM_SIZE; i++) {
        id[i] = random(255);
        EEPROM.write(i, id[i]);
    }    
  }
}

void id_handshake() {
  //Serial.write("Hey there!");
  Serial.write(id, sizeof(id));
  //Serial.write("How are you?");
}

void setup() {
  // seed random
  unsigned long value = millis();
  for (size_t i = 0; i < 4096; i++)
    value += analogRead(i % 32);
  randomSeed(value);
  
  setup_id();
  SoftPWMBegin();
  Serial.begin(BAUD);
  id_handshake();  
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

        //Serial.print([chk, chk_in])
        // validate message via checksum
        if ((chk & 0xFF) == (chk_in & 0xFF)) {

          // handshake check
          //if (!handshake || header->cmd == '9') {
          if (header->cmd == '9') {
            id_handshake();
              /*
               
              bool success = true;
              
              // answer has to contain the id
              for (int i = 0; i < header->data_len; i++) {
                if (EEPROM.read(i) != header->data[i]) {
                  success = false;
                  break;
                  }
                }
              
              // mark handshake as sucess
              if (success) {
                handshake = true;
              }
              
              // redo handshake
              else {
                id_handshake();
              }
              */
            }
              
            // pin commands
            else {
  
              if (header->nr < sizeof(PIN_LIST)) {
                bool result = PIN_LIST[header->nr].receive(header);
                //Serial.print(result);
                //Serial.write(result ? 1 : 0);
              } else {
                //Serial.print(header);
              }
            }
          } else {
              //Serial.print("fail ");// + std::to_string(header));
          }
        
        MSG_SIZE = 0;
      }
    }
  }
}
