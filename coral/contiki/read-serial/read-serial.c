/*
 * Copyright (c) 2006, Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */

/**
 * \file
 *         A very simple Contiki application showing how Contiki reads from uart
 * \author
 *         Tryfon Theodorou
 */

#include "contiki.h"
#include "dev/serial-line.h"
#include <stdio.h> /* For printf() */

#include "dev/uart0.h"  // uart0 gia sky, uart1 gia zolertia
#define UART_BUFFER_SIZE      150 
/*---------------------------------------------------------------------------*/
PROCESS(read_serial_process, "Reading from serial process");
AUTOSTART_PROCESSES(&read_serial_process);
/*---------------------------------------------------------------------------*/

static uint8_t uart_buffer[UART_BUFFER_SIZE];
static uint8_t uart_buffer_index = 0;

/*---------------------------------------------------------------------------*/
int uart_rx_callback(unsigned char c) {
    if(c != '\n' && uart_buffer_index < UART_BUFFER_SIZE){
        uart_buffer[uart_buffer_index++] = c;
    }
    else{
        uart_buffer[uart_buffer_index] = '\0';
        uart_buffer_index = 0;
        printf("%s\n",uart_buffer);
    }

    return 0;
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(read_serial_process, ev, data){

    PROCESS_BEGIN();
  
    /* FOR Z1->uart0  for sky->uart1 */
    uart0_init(BAUD2UBR(115200));       /* set the baud rate as necessary */
    uart0_set_input(uart_rx_callback);  /* set the callback function */

    printf("Start reading\n");

    PROCESS_END();
}
/*---------------------------------------------------------------------------*/
