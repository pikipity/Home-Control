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
 
 device 1  6
 device 2  4
 device 3  2
 note: long -> high
 */

#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>

byte data[1];
int led1=6;
int led2=4;
int led3=2;

void setup(){
  //init serial port
  Serial.begin(9600);
  //init SPI port
  Mirf.spi=&MirfHardwareSpi;
  Mirf.init();
  //set self address
  Mirf.setRADDR((byte *)"serve");
  //set transmiate address
  Mirf.setTADDR((byte *)"client");
  //set set data length
  Mirf.payload=sizeof(byte);
  //init nrf24l01
  Mirf.config();
  //init device
  for(int i=2;i<7;i++){
    pinMode(i,OUTPUT);
    digitalWrite(i,LOW);
  }
}

void loop(){
  //adjust if data has been  recived
  if(!Mirf.isSending() && Mirf.dataReady()){
    //get data from nrf24l01
    Mirf.getData(data);
    byte rece=data[0];
    //adjust device
    switch(rece>>1){
      case 1:
        if(rece&1==1){
          digitalWrite(led1,LOW);
        }else{
          digitalWrite(led1,HIGH);
        }
        break;
      case 2:
        if(rece&1==1){
          digitalWrite(led2,LOW);
        }else{
          digitalWrite(led2,HIGH);
        }
        break;
      case 3:
        if(rece&1==1){
          digitalWrite(led3,LOW);
        }else{
          digitalWrite(led3,HIGH);
        }
        break;
      default:
        break; 
    }
  }
}
