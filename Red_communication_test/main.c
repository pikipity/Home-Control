/*
* 红外接收数据，中断方式，并通过串口发送
*
* 晶振：11.0592M
*/

#include <reg52.h>
#include <MYCHIP.h>

typedef unsigned char uint8;

sbit Ir_Pin = P3^3;

uint8 Ir_Buf[4]={0x00,0xFF,0x16,0xE6}; //用于保存解码结果
uint8 device_info[3]={0,0,0};
unsigned char DeviceNum;
/*
unsigned char code number[]={0xc0,0xf9,0xa4,0xb0,
				             0x99,0x92,0x82,0xf8,
				             0x80,0x90};
							 */
unsigned char Receving;

unsigned char code word1[]={"Device One On"};
unsigned char code word2[]={"Device One Off"};
unsigned char code word3[]={"Device Two On"};
unsigned char code word4[]={"Device Two Off"};
unsigned char code word5[]={"Device Three On"};
unsigned char code word6[]={"Device Three Off"};
unsigned char code word7[]={"                "};
unsigned char code word8[]={"No this device"};
unsigned char open_word[]={"O"};
unsigned char close_word[]={"X"};

/**
 * 等待繁忙标志
*/
void wait(void)
{
	P0 = 0xFF;
	
	do
	{
		RS = 0;
		RW = 1;
		EN = 0;
		EN = 1;
	}while (BUSY == 1);
	EN = 0;
}

/**
 * 写数据
*/
void w_dat(unsigned char dat)
{
	wait();
	EN = 0;
	P0 = dat;
	RS = 1;
	RW = 0;
	EN = 1;
	EN = 0;
}

/**
 * 写命令
*/
void w_cmd(unsigned char cmd)
{
	wait();
	EN = 0;
	P0 = cmd;
	RS = 0;
	RW = 0;
	EN = 1;
	EN = 0;
}

/**
 * 发送字符串到LCD
*/
void w_string(unsigned char addr_start, unsigned char *p)
{
	unsigned char *pp;
	
	pp = p;
	w_cmd(addr_start);
	while (*pp != '\0')
	{
		w_dat(*pp++);
	}
}


/**
 * 初始化1602
*/
void Init_LCD1602(void)
{
	w_cmd(0x01);  // 清屏
	w_cmd(0x38);  // 16*2显示，5*7点阵，8位数据接口
	w_cmd(0x0C);  // 显示器开、光标开、光标允许闪烁
	w_cmd(0x06);  // 文字不动，光标自动右移
}


/*
 * 外部中断初始化
*/
void int1_init(void)
{
	IT1 = 1; //下降沿有效
	EX1 = 1;
	EA = 1;
}

void Timer_init()
{
	TMOD=0x21;
	TH1 = 0xFD;
    TL1 = 0xFD;

    TR1 = 1;
}


/*
 * UART初始化
 * 波特率：9600
*/
void uart_init(void)
{ 
    SCON = 0x50; 
}

/*
 * UART发送一字节
*/
void UART_Send_Byte(uint8 dat)
{
	SBUF = dat;
	while (TI == 0);
	TI = 0;
}


/*
 * 数码管初始化
*/
/*
void LED_init()
{
	ENLED1=0;
	ADDR3=1;
	ADDR0=0;
	ADDR1=1;
	ADDR2=1;
}
*/


/*
 * 获取低电平时间
*/
unsigned int Ir_Get_Low()
{
	TL0 = 0;
	TH0 = 0;
	TR0 = 1;
	while (!Ir_Pin && (TH0&0x80)==0);  
              
	TR0 = 0;           
	return (TH0 * 256 + TL0);
}

/*
 * 获取高电平时间
*/
unsigned int Ir_Get_High()
{
	TL0 = 0;
	TH0 = 0;
	TR0 = 1;
	while (Ir_Pin && (TH0&0x80)==0);

	TR0 = 0;
	return (TH0 * 256 + TL0);
}


main()
{
	Init_LCD1602();
	//LED_init();
	w_string(0x80,close_word);
	w_string(0x81,close_word);
	w_string(0x82,close_word);
	Timer_init();
	uart_init();
	int1_init();

	while (1)
	{
		/*
		DB7=~device_info[0];
		DB6=~device_info[1];
		DB5=~device_info[2];
		*/
		if(RI==1)
		{
			Receving=SBUF;
			switch(Receving>>1)
			{
				case 1:
					device_info[0]=(~(Receving & 0x01))&0x01;
					w_string(0xC0,word7); 
					if(device_info[0]){
						w_string(0xC0,word1);
						w_string(0x80,open_word);
					}else{
						w_string(0xC0,word2);
						w_string(0x80,close_word);
					}
					break;
				case 2:
					device_info[1]=(~(Receving & 0x01))&0x01;
					w_string(0xC0,word7); 
					if(device_info[1]){
						w_string(0xC0,word3);
						w_string(0x81,open_word);
					}else{
						w_string(0xC0,word4);
						w_string(0x81,close_word);
					}
					break;
				case 3:
					device_info[2]=(~(Receving & 0x01))&0x01;
					w_string(0xC0,word7); 
					if(device_info[2]){
						w_string(0xC0,word5);
						w_string(0x82,open_word);
					}else{
						w_string(0xC0,word6);
						w_string(0x82,close_word);
					}
					break;
				default:
					w_string(0xC0,word7); 
					w_string(0xC0,word8);
			}	
			RI=0;
		}
	}
}

void int1_isr() interrupt 2
{
	unsigned int temp;
	char i,j;

	temp = Ir_Get_Low();
	if ((temp < 7833) || (temp > 8755))  //引导脉冲低电平8500~9500us
		return;
	temp = Ir_Get_High();
	if ((temp < 3686) || (temp > 4608))  //引导脉冲高电平4000~5000us
		return;

	for (i=0; i<4; i++) //4个字节
	{
		for (j=0; j<8; j++) //每个字节8位
		{
			temp = Ir_Get_Low();
			if ((temp < 184) || (temp > 737)) //200~800us
				return;

			temp = Ir_Get_High();
			if ((temp < 184) || (temp > 1843)) //200~2000us
				return;

			Ir_Buf[i] >>= 1;
			if (temp > 1032) //1120us
				Ir_Buf[i] |= 0x80;
		}
	}
	//UART_Send_Byte(Ir_Buf[2]);
	switch(Ir_Buf[2])
		{
			case 0x0C:
				w_string(0xC0,word7); 
				if(device_info[0]){
					w_string(0xC0,word2);
					w_string(0x80,close_word);
				}else{
					w_string(0xC0,word1);
					w_string(0x80,open_word);
				}
				device_info[0]=~device_info[0];DeviceNum=(1<<1)|(~(device_info[0])&0x01);UART_Send_Byte(DeviceNum); break;
			case 0x18:
				w_string(0xC0,word7); 
				if(device_info[1]){
					w_string(0xC0,word4);
					w_string(0x81,close_word);
				}else{
					w_string(0xC0,word3);
					w_string(0x81,open_word);
				}
				device_info[1]=~device_info[1];DeviceNum=(2<<1)|(~(device_info[1])&0x01);UART_Send_Byte(DeviceNum); break;
			case 0x5E:
				w_string(0xC0,word7); 
				if(device_info[2]){
					w_string(0xC0,word6);
					w_string(0x82,close_word);
				}else{
					w_string(0xC0,word5);
					w_string(0x82,open_word);
				}
				device_info[2]=~device_info[2];DeviceNum=(3<<1)|(~(device_info[2])&0x01);UART_Send_Byte(DeviceNum); break;
			default:
				w_string(0xC0,word7); 
			    w_string(0xC0,word8);
		}
}