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
unsigned char DeviceNum;
unsigned char code number[]={0xc0,0xf9,0xa4,0xb0,
				             0x99,0x92,0x82,0xf8,
				             0x80,0x90};
unsigned char Receving;


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
void LED_init()
{
	ENLED1=0;
	ADDR3=1;
	ADDR0=0;
	ADDR1=1;
	ADDR2=1;
}


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
	LED_init();
	Timer_init();
	uart_init();
	int1_init();

	while (1)
	{
		if(RI==1)
		{
			Receving=SBUF;
			switch(Receving>>1)
			{
				case 1:DB7=Receving & 0x01;
				case 2:DB6=Receving & 0x01;
				case 3:DB5=Receving & 0x01;
			}	
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
			case 0x0C:DB7=~DB7;DeviceNum=(1<<1)|DB7;UART_Send_Byte(DeviceNum); break;
			case 0x18:DB6=~DB6;DeviceNum=(2<<1)|DB6;UART_Send_Byte(DeviceNum); break;
			case 0x5E:DB5=~DB5;DeviceNum=(3<<1)|DB5;UART_Send_Byte(DeviceNum); break;
		}
}