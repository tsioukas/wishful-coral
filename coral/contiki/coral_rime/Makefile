CONTIKI_PROJECT = coral
all: $(CONTIKI_PROJECT)

TARGET=rm090

CONTIKI = ../../../contiki
CONTIKI_WITH_RIME = 1

#PROJECT_SOURCEFILES = addr.c packet.c neighbor.c 
#flowtable.c packet-buffer.c address.c neighbor-table.c packet-handler.c node-conf.c packet-creator.c
#TARGETDIRS += ../targets
CFLAGS += -DPROJECT_CONF_H=\"coral_conf.h\"

WISHFUL_EXTENSIONS=1

ifeq ($(WISHFUL_EXTENSIONS), 1)
CFLAGS+=-DWISHFUL_EXTENSIONS
APPS += param-repo
endif

include $(CONTIKI)/Makefile.include
