#include <Wire.h>
#include <Arduino.h>
#include <Wifi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <ArduinoCbor.h>

#include <stdint.h>
#include <chrono>
#include <thread>


#include <MLX90640_API.h>
#include <MLX90640_I2C_Driver.h>

const byte MLX90640_address = 0x33; //Default 7-bit unshifted address of the MLX90640

const char* ssid = "VOP2.4";
const char* password = "Marijnsuckt";

const char* host = "Thermal sensor 0x33";

const char* rasp_ip = "192.168.1.31"; //"<rasp-ip>/sensor/debug";
const int rasp_port = 5000;
const char* rasp_path = "/sensor/debug";

#define TA_SHIFT 8 //Default shift for MLX90640 in open air
#define PAGE_SIZE 1536 //size of combination of subpages
#define TEMP_THRESHOLD 30 
#define MLX_I2C_ADDR 0x33
#define FPS 4
#define FRAME_TIME_MICROS (1000000/(4*FPS))

#define OFFSET_MICROS 850

static uint16_t eeMLX90640[832];
float emissivity = 1;
uint16_t frame[834];
static float mlx90640To[768];
float eTa;
paramsMLX90640 mlx90640;

uint16_t sequence_id = 0;

auto frame_time = std::chrono::microseconds(FRAME_TIME_MICROS + OFFSET_MICROS);

void setup() {
  Wire.begin();
  Wire.setClock(400000); //Increase I2C clock speed to 400kHz

  Serial.begin(115200); //Fastest serial as possible
  delay(10);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  //Get device parameters - We only have to do this once

  MLX90640_SetDeviceMode(MLX_I2C_ADDR, 0);
  MLX90640_SetSubPageRepeat(MLX_I2C_ADDR, 0);
  switch(FPS){
      case 1:
          MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b001);
          break;
      case 2:
          MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b010);
          break;
      case 4:
          MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b011);
          break;
      case 8:
          MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b100);
          break;
      case 16:
          MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b101);
          break;
      case 32:
          MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b110);
          break;
      case 64:
          MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b111);
          break;
      default:
          Serial.print("Unsupported framerate: %d");
          Serial.println(FPS);
  }
  
  MLX90640_SetChessMode(MLX_I2C_ADDR);
  MLX90640_DumpEE(MLX_I2C_ADDR, eeMLX90640);
  MLX90640_ExtractParameters(eeMLX90640, &mlx90640);
  Wire.setClock(1000000);
}

void loop() {
  //long startTime = millis();
  
  auto start = std::chrono::system_clock::now();
  MLX90640_GetFrameData(MLX_I2C_ADDR, frame);
  MLX90640_InterpolateOutliers(frame, eeMLX90640);

  eTa = MLX90640_GetTa(frame, &mlx90640);
  MLX90640_CalculateTo(frame, &mlx90640, emissivity, eTa, mlx90640To);

  //auto end = std::chrono::system_clock::now();
  //auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
  //long stopTime = millis();

  HTTPClient http;
  http.begin(rasp_ip, rasp_port, rasp_path);
  http.addHeader("Content-Type", "application/json"); //TODO

  DynamicJsonBuffer jBuffer; //TODO make static
  JsonObject& root = jBuffer.createObject();
  //CborBuffer cBuffer(1000);
  //CborObject root = CborObject(cBuffer);

  //root.set("device_id", MLX90640_address);
  //root.set("device_id", sequence_id);
  root["device_id"] = 65;
  root["sequence"] = sequence_id;
  JsonArray& data = root.createNestedArray("data");
  //CborArray array = CborArray(cBuffer);
  
  for (int i = 0; i < 768; i++) {
     data.add(mlx90640To[i]);
    //uint8_t val;
    //if (mlx90640To[i] >= TEMP_THRESHOLD) {
    //  val = 1;
    //}
    //else {
    //  val = 0;
    //}
    //array.add(val);
  }

  //root.set("array", array);

  char* jsonRaw = (char*)calloc(sizeof(char), root.measureLength() + 1);
  //Serial.println("ROOT MEASURELENGTH");
  //Serial.println(root.measureLength());
  
  //root.prettyPrintTo(Serial);
  
  root.printTo(jsonRaw, root.measureLength() + 1);

  int httpResponseCode = http.POST(jsonRaw);
  //int httpResponseCode = http.POST(root.get("string").asString());
  //int httpResponseCode = http.POST(root.get("integer").asInteger());
  sequence_id++;

  if (httpResponseCode) {
    Serial.print("POST request, httpResponseCode:");
    Serial.println(httpResponseCode);
   }

  auto end = std::chrono::system_clock::now();
  auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

  std::this_thread::sleep_for(std::chrono::microseconds(frame_time - elapsed));

  free(jsonRaw);
  http.end();
  
}