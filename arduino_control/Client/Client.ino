/*
hardware:
 GND -> GND
 VCC -> 3.3V
 CE -> 8
 CSN -> 7
 SCK -> 13
 MOSI -> 11
 MISO -> 12
 IRQ -> none
 
 IRQ   MISO
 MOSI  SCK
 CSN   CE
 VCC   GND
 */

#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>

byte device1_open=3;

void setup(){
  //init serial port
  Serial.begin(9600);
  //init SPI port
  Mirf.spi=&MirfHardwareSpi;
  Mirf.init();
  //set self address
  Mirf.setRADDR((byte *)"client");
  //set transimate address
  Mirf.setTADDR((byte *)"serve");
  //set set data length
  Mirf.payload=sizeof(byte);
  //init nrf24l01
  Mirf.config();
}

void loop(){
  if(Serial.available()>0){
    byte com_data=Serial.read();
    Mirf.send((byte *)&com_data);
  }
}

