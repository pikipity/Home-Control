import java.util.*;
import java.text.*;
import processing.serial.*;

Serial myPort;

String My_name;

PImage bg;
int bg_num;
int max_bg_num;

void draw_player_left(int center_x,int center_y,int head_len,int body_len,boolean arm_move){
  fill(255);
  int center[]={center_x,center_y};
  int half_head_len=Math.round(head_len*0.3);
  int mouth_len=head_len/8*3;
  int half_body_len_1=Math.round(body_len*0.3);
  int half_body_len_2=Math.round(body_len*0.5);
  //background
  stroke(255);
  image(bg,0,0,human_move_range[0],human_move_range[1]);
  //rect(-1,-1,human_move_range[0]+1,human_move_range[1]+1);
  //rect(center[0]-head_len/2-half_head_len,center[1]-head_len-half_head_len,
  //      head_len+half_head_len+half_head_len,half_head_len+head_len+body_len+half_body_len_2*sqrt(2)*sqrt(3)/2);
  stroke(0);
  //head
  rect(center[0]-head_len/2,center[1]-head_len,head_len,head_len);
  quad(center[0]-head_len/2,center[1]-head_len
      ,center[0]+head_len/2,center[1]-head_len
      ,center[0]+head_len/2+half_head_len,center[1]-head_len-half_head_len
      ,center[0]-(head_len/2-half_head_len),center[1]-head_len-half_head_len);
  quad(center[0]+head_len/2,center[1]-head_len
      ,center[0]+head_len/2+half_head_len,center[1]-head_len-half_head_len
      ,center[0]+head_len/2+half_head_len,center[1]-half_head_len
      ,center[0]+head_len/2,center[1]);
  //glasses
  center[1]=center[1]-head_len/3*2;
  line(center[0]-head_len/2,center[1],center[0]-head_len/2+head_len/8,center[1]);
  rect(center[0]-head_len/2+head_len/8,center[1]-head_len/8,head_len/4+head_len/16,head_len/4);
  line(center[0]-head_len/16,center[1],center[0]+head_len/16,center[1]);
  line(center[0]+head_len/2,center[1],center[0]+head_len/2-head_len/8,center[1]);
  rect(center[0]+head_len/16,center[1]-head_len/8,head_len/4+head_len/16,head_len/4);
  line(center[0]+head_len/2,center[1],center[0]+head_len/2+half_head_len,center[1]-half_head_len);
  //mouth
  center[1]=center_y-head_len/3;
  line(center[0]-mouth_len/2,center[1],center[0]+mouth_len/2,center[1]);
  //body
  center[0]=center_x+half_head_len/2;
  center[1]=center_y;
  line(center[0],center[1],center[0],center[1]+body_len);
  if(arm_move){
    line(center[0],center[1]+body_len/3,center[0]+half_body_len_1,center[1]+body_len/3-half_body_len_1);
    line(center[0],center[1]+body_len/3,center[0]-half_body_len_1,center[1]+body_len/3-half_body_len_1);
  }else{
    line(center[0],center[1]+body_len/3,center[0]+half_body_len_1,center[1]+body_len/3+half_body_len_1);
    line(center[0],center[1]+body_len/3,center[0]-half_body_len_1,center[1]+body_len/3+half_body_len_1);
  }
  if(arm_move){
    line(center[0],center[1]+body_len,center[0]+half_body_len_2*sqrt(2)/2,center[1]+body_len+half_body_len_2*sqrt(2)*sqrt(3)/2);
    line(center[0],center[1]+body_len,center[0]-half_body_len_2*sqrt(2)/2,center[1]+body_len+half_body_len_2*sqrt(2)*sqrt(3)/2);
  }else{
    line(center[0],center[1]+body_len,center[0]+half_body_len_2,center[1]+body_len+half_body_len_2);
    line(center[0],center[1]+body_len,center[0]-half_body_len_2,center[1]+body_len+half_body_len_2);
  }
  fill(0);
}

void draw_player_right(int center_x,int center_y,int head_len,int body_len,boolean arm_move){
  fill(255);
  int center[]={center_x,center_y};
  int half_head_len=Math.round(head_len*0.3);
  int mouth_len=head_len/8*3;
  int half_body_len_1=Math.round(body_len*0.3);
  int half_body_len_2=Math.round(body_len*0.5);
  //background
  stroke(255);
  image(bg,0,0,human_move_range[0],human_move_range[1]);
  //rect(center[0]-head_len/2-half_head_len,center[1]-head_len-half_head_len,
  //      head_len+half_head_len+half_head_len,half_head_len+head_len+body_len+half_body_len_2*sqrt(2)*sqrt(3)/2);
  stroke(0);
  //head
  rect(center[0]-head_len/2,center[1]-head_len,head_len,head_len);
  quad(center[0]-head_len/2,center[1]-head_len
      ,center[0]+head_len/2,center[1]-head_len
      ,center[0]+head_len/2-half_head_len,center[1]-head_len-half_head_len
      ,center[0]-(head_len/2+half_head_len),center[1]-head_len-half_head_len);
  quad(center[0]-head_len/2,center[1]-head_len
      ,center[0]-head_len/2-half_head_len,center[1]-head_len-half_head_len
      ,center[0]-head_len/2-half_head_len,center[1]-half_head_len
      ,center[0]-head_len/2,center[1]);
  //glasses
  center[1]=center[1]-head_len/3*2;
  line(center[0]-head_len/2,center[1],center[0]-head_len/2+head_len/8,center[1]);
  rect(center[0]-head_len/2+head_len/8,center[1]-head_len/8,head_len/4+head_len/16,head_len/4);
  line(center[0]-head_len/16,center[1],center[0]+head_len/16,center[1]);
  line(center[0]+head_len/2,center[1],center[0]+head_len/2-head_len/8,center[1]);
  rect(center[0]+head_len/16,center[1]-head_len/8,head_len/4+head_len/16,head_len/4);
  line(center[0]-head_len/2,center[1],center[0]-head_len/2-half_head_len,center[1]-half_head_len);
  //mouth
  center[1]=center_y-head_len/3;
  line(center[0]-mouth_len/2,center[1],center[0]+mouth_len/2,center[1]);
  //body
  center[0]=center_x-half_head_len/2;
  center[1]=center_y;
  line(center[0],center[1],center[0],center[1]+body_len);
  if(arm_move){
    line(center[0],center[1]+body_len/3,center[0]+half_body_len_1,center[1]+body_len/3-half_body_len_1);
    line(center[0],center[1]+body_len/3,center[0]-half_body_len_1,center[1]+body_len/3-half_body_len_1);
  }else{
    line(center[0],center[1]+body_len/3,center[0]+half_body_len_1,center[1]+body_len/3+half_body_len_1);
    line(center[0],center[1]+body_len/3,center[0]-half_body_len_1,center[1]+body_len/3+half_body_len_1);
  }
  if(arm_move){
    line(center[0],center[1]+body_len,center[0]+half_body_len_2*sqrt(2)/2,center[1]+body_len+half_body_len_2*sqrt(2)*sqrt(3)/2);
    line(center[0],center[1]+body_len,center[0]-half_body_len_2*sqrt(2)/2,center[1]+body_len+half_body_len_2*sqrt(2)*sqrt(3)/2);
  }else{
    line(center[0],center[1]+body_len,center[0]+half_body_len_2,center[1]+body_len+half_body_len_2);
    line(center[0],center[1]+body_len,center[0]-half_body_len_2,center[1]+body_len+half_body_len_2);
  }
  fill(0);
}


//count for animation
int move_count=0;
int stay_count=0;
int target_count=0;
int target_R=20;
int fps=60;
PFont font;
//value for human
int human_move_range[]={480,480};
int[] human_len=new int[2];
int[] human_loca=new int[2];
boolean move=false;
boolean move_motion=false;
boolean face=true;//true:left, false:right
//value for mouse control
boolean hold=false;
boolean go=false;
int target[]={0,0};
//value talk
String talk="Hello";
int talk_count=0;
int talk_num;
//begin introduction
boolean begin=true;
String[] begin_text;
//stay talk
boolean stay_talk=false;
String[] stay_text;
Date dNow = new Date( );
SimpleDateFormat day=new SimpleDateFormat ("yyyy.MM.dd");
SimpleDateFormat time_format=new SimpleDateFormat ("HH:mm:ss");
SimpleDateFormat complex_format=new SimpleDateFormat ("yyyy.MM.dd\nHH:mm:ss");
//press talk
boolean press_talk=false;
String[] press_text;
//communication
String[] config; 
String[] mapping;
boolean commu=false;
String input_text="";
String output_text="";
String master_name="";
boolean input_name=false;
boolean input_name_adjust=false;

void setup(){
  if(Serial.list().length>0){
  if(System.getProperties().getProperty("os.name").contains("Mac OS X")){
      myPort=new Serial(this,"/dev/tty.usbmodem1411",9600);
  }else if(System.getProperties().getProperty("os.name").contains("Windows")){
    String portName=Serial.list()[0];
    myPort=new Serial(this,portName,9600);
  }
  }
  //get config
  mapping=loadStrings("map.txt");
  press_text=loadStrings("press_text.txt");
  stay_text=loadStrings("stay_text.txt");
  begin_text=loadStrings("begin_text.txt");
  config=loadStrings("config.txt");
  //get human name
  My_name=config[0];
  My_name=My_name.substring(My_name.indexOf(":")+1,My_name.length());
  begin_text[0]="I'm "+My_name;
  //get master name
  master_name=config[1];
  master_name=master_name.substring(master_name.indexOf(":")+1,master_name.length());
  //get background number
  bg_num=Integer.parseInt(config[2].substring(config[2].indexOf(":")+1,config[2].length()));
  bg=loadImage("bg"+Integer.toString(bg_num)+".png");
  max_bg_num=Integer.parseInt(config[3].substring(config[3].indexOf(":")+1,config[3].length()));
  //get human length
  human_len[0]=Integer.parseInt(config[4].substring(config[4].indexOf(":")+1,config[4].length()));
  human_len[1]=Integer.parseInt(config[5].substring(config[5].indexOf(":")+1,config[5].length()));
  //get human init location
  human_loca[0]=Integer.parseInt(config[6].substring(config[6].indexOf(":")+1,config[6].length()));
  human_loca[1]=Integer.parseInt(config[7].substring(config[7].indexOf(":")+1,config[7].length()));
  //init input text
  if(master_name.length()==0){
    input_text="My name is ";
  }
  //init game
  size(human_move_range[0],human_move_range[1]+20);
  frameRate(fps);
  smooth();
  strokeJoin(ROUND);
  background(255);
  font=loadFont("SansSerif-15.vlw");
  textFont(font);
  //init human
  draw_player_left(human_loca[0],human_loca[1],human_len[0],human_len[1],move_motion);
}

void draw(){
  check_go();
  check_mouse();
  draw_human();
  draw_text();
  draw_target();
  check_talk();
  text_input_area();
}

void text_input_area(){
  fill(255);
  rect(0,human_move_range[1],human_move_range[0],20);
  fill(0);
  textAlign(LEFT);
  text(input_text+(frameCount/10 % 2 == 0 ? "_" : ""), 0, human_move_range[1],human_move_range[0],20);
}

void keyPressed() {
  if (key != CODED) {
    switch(key) {
    case BACKSPACE:
      input_text = input_text.substring(0,max(0,input_text.length()-1));
      break;
    case TAB:
      input_text += "    ";
      break;
    case ENTER:
    case RETURN:
      if(input_text.toLowerCase().contains("open")&&input_text.toLowerCase().contains("device")){
        if(input_text.toLowerCase().contains("one") || input_text.contains("1")){
          myPort.write(0x02);
          output_text="Let's Open device One";
        }else if(input_text.toLowerCase().contains("two") || input_text.contains("2")){
          myPort.write(0x04);
          output_text="Let's Open device Two";
        }else if(input_text.toLowerCase().contains("three") || input_text.contains("3")){
          myPort.write(0x06);
          output_text="Let's Open device Three";
        }else{
          output_text="Cannot find this device";
        }    
        input_text="";
      }else if(input_text.toLowerCase().contains("close")&&input_text.toLowerCase().contains("device")){
        if(input_text.toLowerCase().contains("one") || input_text.contains("1")){
          myPort.write(0x03);
          output_text="Let's Close device One";
        }else if(input_text.toLowerCase().contains("two") || input_text.contains("2")){
          myPort.write(0x05);
          output_text="Let's Close device Two";
        }else if(input_text.toLowerCase().contains("three") || input_text.contains("3")){
          myPort.write(0x07);
          output_text="Let's Close device Three";
        }else{
          output_text="Cannot find this device";
        }
        input_text="";
      }else
      if(!begin){
        if(input_name){
          input_name=false;
          if(input_text.toLowerCase().contains("is")){
            master_name=input_text.substring(input_text.toLowerCase().indexOf("is"),input_text.length());
            if(master_name.substring(0,Math.min(3,master_name.length())).contains(" ")){
              master_name=master_name.substring(Math.min(3,master_name.length()),master_name.length());
            }else{
              master_name=master_name.substring(2,master_name.length());
            }
          }else{
            master_name=input_text;
          }
          output_text="Is your name \""+master_name+"\"?(y or n)";
          input_name_adjust=true;
          input_text="Y";
        }else if(input_name_adjust){
          input_name_adjust=false;
          if (input_text.toLowerCase().contains("y")){
            output_text="Hello, "+master_name;
            config[1]="master_name:"+master_name;
            saveStrings("config.txt", config);
            input_text="";
          }else{
            output_text="What is your name?";
            input_name=true;
            input_text="My name is ";
          }
        }else{
          adjust_input_text();
        }
      }else{
        output_text="You don't want to listen me?\nOK. I stop..";
        begin=false;
        if(master_name.length()==0){
          input_text="My name is ";  
        }else{
          input_text="";
        }
      }
      commu=true;
      talk_count=0;
      break;
    case ESC:
    case DELETE:
      break;
    default:
      input_text += key;
    }
  }
}

void adjust_input_text(){
  if(input_text.toLowerCase().contains(" means ")){
          int N=mapping.length;
          mapping=Arrays.copyOf(mapping,N+1);
          mapping[N]=input_text.substring(0,input_text.toLowerCase().indexOf(" means ")).toLowerCase()
                     +":"
                     +input_text.substring(input_text.toLowerCase().indexOf(" means ")+7,input_text.length());
          saveStrings("map.txt",mapping);
          output_text="Thank you!\nNow, I know "+input_text;
          input_text="";
        }else if(input_text.toLowerCase().contains("background")){
          String temp_check=input_text.substring(input_text.toLowerCase().indexOf("background")+10,input_text.length())
                            .replace(" ","");
          if(temp_check.equals("")){
            bg_num++;
            if(bg_num>max_bg_num){
              bg_num=1;
            }
            bg=loadImage("bg"+Integer.toString(bg_num)+".png");
            output_text="Change background\nI like it! :-)\nI draw it by myself.";
            input_text="";
          }else{
            try{
              bg_num=Integer.parseInt(temp_check);
            }catch (NumberFormatException e) {
              bg_num=max_bg_num+1;
            }
            if(bg_num<=max_bg_num && bg_num>0){
              bg=loadImage("bg"+Integer.toString(bg_num)+".png");
              output_text="Change background\nI like it! :-)\nI draw it by myself.";
              input_text="";
            }else{
              output_text="I don't have this background...\nYou can use following sentence\nto change background:\nbackground n (0<n<"+Integer.toString(max_bg_num)+")";
              input_text="";
            }
          }
        }else if(input_text.toLowerCase().contains("time") ||
                (input_text.toLowerCase().contains("time") && input_text.toLowerCase().contains("?")) ||
                (input_text.toLowerCase().contains("time") && input_text.toLowerCase().contains("what"))){
              output_text=complex_format.format(dNow);
          if(Integer.parseInt(output_text.substring(11,13))==23 || Integer.parseInt(output_text.substring(11,13))<7){
              output_text=output_text+"\nGo to sleep, now!!";
          }
          input_text="";
        }else if(input_text.toLowerCase().contains("name") && input_text.toLowerCase().contains("your")){
          output_text="My name is \""+My_name+"\"\nYeah!!!";
        }else if(input_text.toLowerCase().contains("name") && input_text.toLowerCase().contains("my")){
          if(master_name.length()==0 && !input_text.toLowerCase().contains("is")){
            output_text="Sorry\nCould you please\ntell me your name?";
            input_text="My name is ";
            input_name=true;
          }else if(input_text.toLowerCase().contains("is")){
            master_name=input_text.substring(input_text.toLowerCase().indexOf("is"),input_text.length());
            if(master_name.substring(0,Math.min(3,master_name.length())).contains(" ")){
              master_name=master_name.substring(Math.min(3,master_name.length()),master_name.length());
            }else{
              master_name=master_name.substring(2,master_name.length());
            }
            output_text="Is your name \""+master_name+"\"?(y or n)";
            input_text="Y";
            input_name_adjust=true;
          }else{
            output_text="I remember your name is "+master_name+".\nI have a good memery. :-)";
            input_text="";
          }
        }
        else{
          for(int i=0;i<mapping.length;i++){
            if(mapping[i].contains(":")){
              boolean ok_get_mapping=false;
              String key_word=mapping[i].substring(0,mapping[i].indexOf(":"));
              if(!key_word.contains("&&")){
                ok_get_mapping=input_text.toLowerCase().contains(mapping[i].substring(0,mapping[i].indexOf(":")));
              }else{
                String[] results=key_word.split("&&");
                for(int j=0;j<results.length;j++){
                  ok_get_mapping=true;
                  ok_get_mapping=ok_get_mapping && input_text.toLowerCase().contains(results[j]);
                  if(!ok_get_mapping){
                    break;
                  }
                }
              }
              if(ok_get_mapping){
                output_text=mapping[i].substring(mapping[i].indexOf(":")+1,mapping[i].length());
                break;      
              }else{
                output_text="Did you say \""+input_text+"\"?\nI don't understand..."
                            +"\nYou can tell me the meaning by\n"
                            +"\"WORDS means MEANING\"";   
              }
            }
          }
          input_text="";
        }
}

void check_talk(){
  if(commu){
    stay_talk=false;
    press_talk=false;
    if(talk_count==0){
      talk=output_text;
      talk_count++;
    }else if(talk_count==180){
      talk="";
      output_text="";
      talk_num=0;
      talk_count=0;
      commu=false;
    }else{
      talk_count++;
    }
  }
  if(press_talk){
    if(talk_num<press_text.length && talk_num>=0){
        stay_talk=false;
        if(talk_count==0){
          talk=press_text[talk_num];
        }else if(talk_count==180){
          talk="";
          talk_num=0;
          talk_count=0;
          press_talk=false;
        }
        talk_count++;
      }
  }
  if(stay_talk){
    talk_count++;
    if(talk_count==180){
      talk_count=0;
      if(talk_num<stay_text.length && talk_num>=0){
        talk=stay_text[talk_num];
        talk_num=stay_text.length+1;
      }else{
        talk="";
        talk_num=0;
        talk_count=0;
        stay_talk=false;
      }
    }
  }
  if(begin){
    talk_count++;
    if(talk_count==240){
      talk_count=0;
      if(talk_num<begin_text.length){
        talk=begin_text[talk_num];
        talk_num++;
      }else{
        talk="";
        talk_count=0;
        talk_num=0;
        begin=false;
        if(master_name.length()==0){
          commu=true;
          output_text="Could you please\ntell me your name?";
          input_text="My name is ";
          input_name=true;
        }else{
          commu=true;
          output_text="You can press\nmouse to move me, "+master_name+". :-)";
        }
      }
    }
  }
}

void mouseClicked(){
  if(((mouseX>=human_loca[0]-human_len[0]/2) &&
         (mouseX<=human_loca[0]+human_len[0]/2+Math.round(human_len[0]*0.3)) &&
         (mouseY>=human_loca[1]-human_len[0]-Math.round(human_len[0]*0.3)) &&
         (mouseY<=human_loca[1]+human_len[1]+Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2) &&
         face) ||
         ((mouseX>=human_loca[0]-human_len[0]/2-Math.round(human_len[0]*0.3)) &&
          (mouseX<=human_loca[0]+human_len[0]/2) &&
          (mouseY>=human_loca[1]-human_len[0]-Math.round(human_len[0]*0.3)) &&
          (mouseY<=human_loca[1]+human_len[1]+Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2) &&
          !face)){
            if(!press_talk && !begin){
              press_talk=true;
              talk_num=int(random(0,press_text.length));
              talk_count=0;
            }
          }else /*if(mouseY>=human_len[0]+Math.round(human_len[0]*0.3) &&
           mouseY<=human_move_range[1] &&
           mouseX>=human_len[0]/2 &&
           mouseX<=human_move_range[0]-human_len[0]/2)*/{
             go=true;
             if(target[0]==0 && target[1]==0){
               target[0]=mouseX;
               target[1]=Math.round(mouseY-human_len[1]-Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2);
             }else{
               target[0]=mouseX;
               target[1]=Math.round(mouseY-human_len[1]-Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2);
             }
          }
}

void draw_text(){
  if(talk.contains("!master_name")){
             talk=talk.replace("!master_name",master_name);
         }
         if(talk.contains("!my_name")){
             talk=talk.replace("!my_name",My_name);
          }
          if(talk.contains("\\n")){
             talk=talk.replace("\\n","\n");
           }
           if(talk.contains("!time")){
             talk=talk.replace("!time",time_format.format(dNow));
             if(Integer.parseInt(time_format.format(dNow).substring(0,2))==23 || Integer.parseInt(time_format.format(dNow).substring(0,2))<7){
               talk=talk+"\nGo to sleep, now!!";
             }
           }
           if(talk.contains("!day")){
              talk=talk.replace("!day",day.format(dNow));
            }
            
  if(human_loca[0]>human_move_range[0]-human_loca[0]){
    fill(0);
    textAlign(RIGHT);
    if(face)
    {
      text(talk,human_loca[0]-human_len[0]/2-talk.length()*10-Math.round(human_len[0]*0.3),human_loca[1]-human_len[0]/2,talk.length()*10,human_len[0]*2);
    }else{
      text(talk,human_loca[0]-human_len[0]/2-Math.round(human_len[0]*0.3)-talk.length()*10-Math.round(human_len[0]*0.3),human_loca[1]-human_len[0]/2,talk.length()*10,human_len[0]*2);
    }
  }else{
    textAlign(LEFT);
    if(!face){
      text(talk,human_loca[0]+human_len[0]/2+Math.round(human_len[0]*0.3),human_loca[1]-human_len[0]/2,talk.length()*10,human_len[0]*2);
    }else{
      text(talk,human_loca[0]+human_len[0]/2+Math.round(human_len[0]*0.3)+Math.round(human_len[0]*0.3),human_loca[1]-human_len[0]/2,talk.length()*10,human_len[0]*2);
    }
  }
}


void check_mouse(){
  if(mousePressed){
    if(!press_talk && !begin){
        press_talk=true;
        talk_num=int(random(0,press_text.length));
        talk_count=0;
     }
    if(hold){
      move=true;
      if(human_loca[0]!=mouseX || human_loca[1]!=mouseY){
        if(human_loca[0]-mouseX>0){
          face=true;
        }else{
          face=false;
        }
        stroke(255);
        fill(255);
        image(bg,0,0,human_move_range[0],human_move_range[1]);
        //rect(human_loca[0]-human_len[0]/2-Math.round(human_len[0]*0.3),human_loca[1]-human_len[0]-Math.round(human_len[0]*0.3),
        //human_len[0]+Math.round(human_len[0]*0.3)+Math.round(human_len[0]*0.3),Math.round(human_len[0]*0.3)+human_len[0]+human_len[1]+Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2);
        fill(0);
        stroke(0);
        if(mouseY>=human_len[0]+Math.round(human_len[0]*0.3) &&
           mouseY<=human_move_range[1]-human_len[1]-Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2 &&
           mouseX>=human_len[0]/2 &&
           mouseX<=human_move_range[0]-human_len[0]/2){
          human_loca[0]=mouseX;
          human_loca[1]=mouseY;
        }else{
          if(mouseX<human_len[0]/2){
            human_loca[0]=human_len[0]/2;
          }
          if(mouseX>human_move_range[0]-human_len[0]/2){
            human_loca[0]=human_move_range[0]-human_len[0]/2;
          }
          if(mouseY<human_len[0]+Math.round(human_len[0]*0.3)){
            human_loca[1]=human_len[0]+Math.round(human_len[0]*0.3);
          }
          if(mouseY>human_move_range[1]-human_len[1]-Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2){
            human_loca[1]=Math.round(human_move_range[1]-human_len[1]-Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2);
          }
        }
      }
    }else{
      if(((mouseX>=human_loca[0]-human_len[0]/2) &&
         (mouseX<=human_loca[0]+human_len[0]/2+Math.round(human_len[0]*0.3)) &&
         (mouseY>=human_loca[1]-human_len[0]-Math.round(human_len[0]*0.3)) &&
         (mouseY<=human_loca[1]+human_len[1]+Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2) &&
         face) ||
         ((mouseX>=human_loca[0]-human_len[0]/2-Math.round(human_len[0]*0.3)) &&
          (mouseX<=human_loca[0]+human_len[0]/2) &&
          (mouseY>=human_loca[1]-human_len[0]-Math.round(human_len[0]*0.3)) &&
          (mouseY<=human_loca[1]+human_len[1]+Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2) &&
          !face)){
           hold=true;
       }else{
         hold=false;
       }
    }
  }else{
    hold=false;
    if(go){
      move=true;
    }else{
      move=false;
      move_motion=false;
    }
  }
  if(face){
      draw_player_left(human_loca[0],human_loca[1],human_len[0],human_len[1],move_motion);
   }else{
      draw_player_right(human_loca[0],human_loca[1],human_len[0],human_len[1],move_motion);
   }
   draw_target();
   draw_text();
}

void check_go(){
  if(go){
    stroke(255);
    fill(255);
    image(bg,0,0,human_move_range[0],human_move_range[1]);
    //rect(human_loca[0]-human_len[0]/2-Math.round(human_len[0]*0.3),human_loca[1]-human_len[0]-Math.round(human_len[0]*0.3),
    //human_len[0]+Math.round(human_len[0]*0.3)+Math.round(human_len[0]*0.3),Math.round(human_len[0]*0.3)+human_len[0]+human_len[1]+Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2);
    fill(0);
    stroke(0);
    if(target[0]-human_loca[0]<0){
      face=true;
    }else{
      face=false;
    }
    human_loca[0]+=Math.round((target[0]-human_loca[0])*0.02);
    human_loca[1]+=Math.round((target[1]-human_loca[1])*0.02);
    if(Math.round((target[0]-human_loca[0])*0.02)==0 && Math.round((target[1]-human_loca[1])*0.02)==0){
      go=false;
      target_R=20;
      target_count=0;
      target[0]=0;
      target[1]=0;
    }
    move=true;
  }
}

void draw_target(){
  if(go){
    target_count++;
    if(target_count==3){
      target_count=0;
      target_R--;
      if(target_R==0){
        target_R=20;
      }
    }
      stroke(255,0,0);
      fill(255,0,0,0);
      ellipse(target[0],target[1]+human_len[1]+Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2,target_R,target_R);
      fill(0);
      stroke(0);
  }
}

void draw_human(){
  if(move){
    stay_count=0;
    move_count++;
    if(move_count==Math.round(fps*15/60)){
      move_count=0;
      move_motion=!move_motion;
      if(face){
        draw_player_left(human_loca[0],human_loca[1],human_len[0],human_len[1],move_motion);
      }else{
        draw_player_right(human_loca[0],human_loca[1],human_len[0],human_len[1],move_motion);
      }
    }
  }else{
    move_count=0;
    stay_count++;
    if(stay_count==fps){
      stay_count=0;
      if(Math.random()<0.2){
        face=!face;
        if(face){
          draw_player_left(human_loca[0],human_loca[1],human_len[0],human_len[1],move_motion);
        }else{
          draw_player_right(human_loca[0],human_loca[1],human_len[0],human_len[1],move_motion);
        }
      }
      if(Math.random()<0.2){
        int random_x=(int)(Math.random()*human_move_range[0]);
        int random_y=(int)(Math.random()*human_move_range[1]);
        if(random_y>=human_len[0]+Math.round(human_len[0]*0.3) &&
           random_y<=human_move_range[1] &&
           random_x>=human_len[0]/2 &&
           random_x<=human_move_range[0]-human_len[0]/2){
             go=true;
             if(target[0]==0 && target[1]==0){
               target[0]=random_x;
               target[1]=Math.round(random_y-human_len[1]-Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2);
             }else{
               target[0]=random_x;
               target[1]=Math.round(random_y-human_len[1]-Math.round(human_len[1]*0.5)*sqrt(2)*sqrt(3)/2);
             }
          }
      }
      if(Math.random()<0.7){
        if(!stay_talk && !begin){
          stay_talk=true;
          talk_num=int(random(0,stay_text.length));
          talk_count=0;
        }
      }
    }
  }
}
