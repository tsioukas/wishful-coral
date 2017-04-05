__author__ = "Piotr Gawlowicz"
__copyright__ = "Copyright (c) 2015, Technische Universitat Berlin"
__version__ = "0.1.0"
__email__ = "gawlowicz@tkn.tu-berlin.de"


#Definition of Local Control Program
def lcrec(controller):
    #do all needed imports here!!!
    import time
    import datetime

    msgNum = 112

    @controller.set_default_callback()
    def default_callback(data):
        print(("\nLC_REC: {}, Id:{} - STARTED".format(controller.name, controller.id)))

        print ("LC_REC: default_callback called")
        #those will be called "automatically"???????????
        print(("LC_REC: lc sending..: {}". data))
        up_message = "lc-->gc:"
        controller.send_upstream({"george_num" :up_message})
        msgNum+=100

        print(("LC_REC:  {}, Id: {} - STOPPED".format(controller.name, controller.id)))
