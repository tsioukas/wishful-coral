CONTIKI = ../../..
APPS = powertrace collect-view
CONTIKI_PROJECT = udp-sender udp-sink
PROJECT_SOURCEFILES += collect-common.c

CFLAGS += -DPROJECT_CONF_H=\"project-conf.h\"

ifeq ($(MAKE_WITH_NON_STORING),1)
CFLAGS += -DWITH_NON_STORING=1
endif

WISHFUL_EXTENSIONS=1
DMA_APP=0
TAISC_CHAIN=Wishful
TAISC_DEBUG=default

#ifneq (,$(findstring yes,$(4COOJA)))
	CFLAGS += -DWITH_COOJA
#endif


# TAISC specific stuff
WITH_TAISC=0


ifeq ($(WISHFUL_EXTENSIONS), 1)
CFLAGS+=-DWISHFUL_EXTENSIONS
APPS += param-repo
endif

ifeq ($(WITH_TAISC), 1)
CFLAGS+=-DWITH_TAISC
endif

ifdef PERIOD
CFLAGS=-DPERIOD=$(PERIOD)
endif

all: $(CONTIKI_PROJECT)

CONTIKI_WITH_IPV6 = 1
include $(CONTIKI)/Makefile.include
