#ifndef _USART_H
#define _USART_H

#include <stdio.h>
#include <stm32f10x.h>

void Rcc_Configuration(void);
void UsartGPIO_Configuration(void);
void usart_Configuration(void);
void UsartGPIO_CTRT_Configuration(void);
void USART_CTRT_Configuartion(void);

#endif /*_USART_H*/
