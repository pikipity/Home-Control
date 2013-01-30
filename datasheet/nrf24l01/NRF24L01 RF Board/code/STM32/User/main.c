#include <stm32f10x.h>
#include "usart.h"
#include "NRF24L01.h"

#define Send	1			//发送
#define Receive	0			//接收

/*-----------------------------------------------------*/
/*这里是控制发送还是接收的变量-----Here control sending or receiving variable */
u8 Mode = Send;
//u8 Mode = Receive;
/*-----------------------------------------------------*/
extern u8 RX_BUF[];
extern u8 TX_BUF[];


void  Delay (uint32_t nCount)
{
  for(; nCount != 0; nCount--);
}

void GPIO_Configuration_key(void);
void LED_indicate(u8 value);

int main(void)
{
	GPIO_InitTypeDef GPIO_InitStruct; 

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOF,ENABLE);
	GPIO_InitStruct.GPIO_Pin = GPIO_Pin_6 | GPIO_Pin_7;
	GPIO_InitStruct.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStruct.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOF, &GPIO_InitStruct);
	GPIO_WriteBit(GPIOF, GPIO_Pin_6 | GPIO_Pin_7, Bit_RESET);
	
	usart_Configuration();

	nRF24L01_Initial();
	printf("USART1测试成功!NRF2401初始化成功!\r\n");

	GPIO_Configuration_key();
//	printf("\r\n接收到数据：%s\r\n",RX_BUF1);
	if(Mode == Send)
	{
		printf("nRF24L01发送模式\r\n");	
		
	}
	else if(Mode == Receive)
		{
			RX_Mode();
			printf("nRF24L01接收模式\r\n");
		}
	while(1)
	{

		if(Mode == Send)
		{

			//TX_Mode();
			if(!(GPIOC->IDR & 0x0001))
			{
				TX_BUF[0]=1;
			}
			else if(!(GPIOC->IDR & 0x0002))
			{
				TX_BUF[0]=2;
			}
			else if(!(GPIOC->IDR & 0x0008))
			{
				TX_BUF[0]=3;
			}
			else if(!(GPIOC->IDR & 0x0004))
			{
				TX_BUF[0]=4;
			}
			else if(!(GPIOG->IDR & 0x0100))
			{
				TX_BUF[0]=5;
			}
			else if(!(GPIOG->IDR & 0x0040))
			{
				TX_BUF[0]=0;
			}
			LED_indicate(TX_BUF[0]);	
			NRF24L01_Send();
		}


		else if(Mode == Receive)
		{
			NRF24L01_Receive();
			LED_indicate(RX_BUF[0]);
		}
	}
}


void LED_indicate(u8 value)
{

	switch(value)
	{
	case 0:
	  GPIO_SetBits(GPIOF , GPIO_Pin_6);
  	GPIO_SetBits(GPIOF , GPIO_Pin_7);
  	GPIO_SetBits(GPIOF , GPIO_Pin_8);
  	GPIO_SetBits(GPIOF , GPIO_Pin_9);
  	Delay(0xfffff);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_6);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_7);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_8);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_9);
  	Delay(0xfffff);
		break;
	case 1:
	  GPIO_SetBits(GPIOF , GPIO_Pin_6);
  	Delay(0xfffff);
	  GPIO_ResetBits(GPIOF , GPIO_Pin_6);
	  Delay(0xfffff);
		break;
	case 2:
  	GPIO_SetBits(GPIOF , GPIO_Pin_7);
  	Delay(0xfffff);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_7);
  	Delay(0xfffff);
		break;
	case 3:
	  GPIO_SetBits(GPIOF , GPIO_Pin_8);
  	Delay(0xfffff);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_8);
  	Delay(0xfffff);
		break;
	case 4:
	  GPIO_SetBits(GPIOF , GPIO_Pin_9);
  	Delay(0xfffff);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_9);
  	Delay(0xfffff);
		break;
	case 5:
	  GPIO_SetBits(GPIOF , GPIO_Pin_6);
	  Delay(0xfffff);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_6);

	  GPIO_SetBits(GPIOF , GPIO_Pin_7);
	  Delay(0xfffff);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_7);

	  GPIO_SetBits(GPIOF , GPIO_Pin_8);
	  Delay(0xfffff);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_8);

	  GPIO_SetBits(GPIOF , GPIO_Pin_9);
	  Delay(0xfffff);
  	GPIO_ResetBits(GPIOF , GPIO_Pin_9);
		break;
	}
}



void GPIO_Configuration_key(void)
{
  GPIO_InitTypeDef GPIO_InitStructure;
  
  RCC_APB2PeriphClockCmd( RCC_APB2Periph_GPIOC | RCC_APB2Periph_GPIOF | RCC_APB2Periph_GPIOG , ENABLE); 						 
/**
 *  LED1 -> PF6 , LED2 -> PF7 , LED3 -> PF8 , LED4 -> PF9
 */					 
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_6 | GPIO_Pin_7 | GPIO_Pin_8 | GPIO_Pin_9;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 
  GPIO_Init(GPIOF, &GPIO_InitStructure);

  /* Key */
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_0 | GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU; 
  GPIO_Init(GPIOC, &GPIO_InitStructure);

  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_6 | GPIO_Pin_8;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_Init(GPIOG, &GPIO_InitStructure);
}

