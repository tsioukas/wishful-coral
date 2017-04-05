/**
 * \file
 *         coral.h Main CORAL mote source code
 * \author
 *         Tryfon Theodorou <tryfonthe@gmail.com>
 */
  
#ifndef CORAL_H_
#define CORAL_H_

#include "contiki.h"
#include <stdio.h>
#include <stdlib.h>
#include "dev/serial-line.h"  /* ??? maybe I can remove */
#include "net/rime/rime.h"
#include "mesh.h"
#include "route.h"
#include "net/linkaddr.h"  


#include "dev/button-sensor.h"
#include "dev/leds.h"

#ifdef WISHFUL_EXTENSIONS
        #include "../apps/param-repo/param-repo.h"
#endif

#define DEBUG 1
#if DEBUG 
   #define PRINTF(...) printf(__VA_ARGS__)
#else
   #define PRINTF(...)
#endif

#ifdef Z1
    #include "dev/uart0.h"  // uart0 for zolertia
#elif defined SKY
    #include "dev/uart1.h"  // uart1 for sky
#endif

#define UART_BUFFER_SIZE      50 
 
#define BC_CHANNEL 100     // Broadcast Channel
#define UC_CHANNEL 101     // 

 #endif
