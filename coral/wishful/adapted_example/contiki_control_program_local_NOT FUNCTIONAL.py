"""
contiki_local_controller.py: Example implementation of local control program for Contiki

Usage:
   contiki_local_controller.py [options] [-q | -v]

Options:
   --logfile name      Name of the logfile
   --config configFile Config file path

Example:
   ./contiki_local_controller -v --config ./config.yaml 

Other options:
   -h, --help          show this help message and exit
   -q, --quiet         print less text
   -v, --verbose       print more text
   --version           show version and exit
"""


import wishful_upis as upis

import signal
import sys, os
import datetime
import logging
import time
import yaml
import wishful_agent

__author__ = "Peter Ruckebusch + ALTERATIONS BY LEFTERIS & GEORGE"
__copyright__ = "Copyright (c) 2016, Ghent University, iMinds"
__version__ = "0.1.0"
__email__ = "peter.ruckebusch@intec.ugent.be"

log = logging.getLogger('wishful_agent.main')

agent = wishful_agent.Agent(local=True)
control_engine = agent.get_local_controller()


@control_engine.set_default_callback()
def default_callback(cmd, data):
    print("{} DEFAULT CALLBACK : Cmd: {}, Returns: {}".format(
        datetime.datetime.now(), cmd, data))

def print_response(data):
    print("{} Specific callback for function call; Print response : {}".format(
        datetime.datetime.now(), data))


def main(args):
    log.debug(args)

    config_file_path = args['--config']
    config = None
    with open(config_file_path, 'r') as f:
        config = yaml.load(f)

    agent.load_config(config)
    agent.run()

    # control loop
    #while True:
        #print("\nNext iteration:")
        
        # execute non-blocking function immediately
        #control_engine.blocking(False).radio.iface("lowpan0").set_rxchannel(26)

 	    #execute non-blocking function immediately (apo to simple ekteleitai mono ston local node)
 	    
 	    
 	    
        
        #control_engine.blocking(False).radio.iface("wlan0").set_power(12)
        
        
        # remember: wlan0 in a PC does NOT exist (no wi-fi)
        #control_engine.blocking(False).net.iface("wlan0").get_iface_ip_addr("wlan0")
        
        
        
        
        # execute non-blocking function immediately, with specific callback
        #power=control_engine.callback(print_response).radio.iface("wlan0").get_power()
        #print ("George: power ===== " + str(power) )
        # execute non-blocking function immediately, with specific callback
        #control_engine.callback(print_response).radio.iface("lowpan0").get_rxchannel()

        # schedule non-blocking function delay
        #control_engine.delay(3).radio.iface("lowpan0").set_rxchannel(11)

        # schedule non-blocking function exec time with default callback
        #exec_time = datetime.datetime.now() + datetime.timedelta(seconds=6)
        #control_engine.exec_time(exec_time).radio.iface("lowpan0").get_rxchannel()

        # execute blocking function immediately
        #result = control_engine.radio.iface("lowpan0").get_rxchannel()
        #print("{} Channel is: {}".format(datetime.datetime.now(), result))

        #time.sleep(15)


if __name__ == "__main__":
    try:
        from docopt import docopt
    except:
        print("""
        Please install docopt using:
            pip install docopt==0.6.1
        For more refer to:
        https://github.com/docopt/docopt
        """)
        raise

    args = docopt(__doc__, version=__version__)

    log_level = logging.INFO  # default
    if args['--verbose']:
        log_level = logging.DEBUG
    elif args['--quiet']:
        log_level = logging.ERROR

    logfile = None
    if args['--logfile']:
        logfile = args['--logfile']

    logging.basicConfig(filename=logfile, level=log_level,
                        format='%(asctime)s - %(name)s.%(funcName)s() - %(levelname)s - %(message)s')

    try:
        main(args)
    except KeyboardInterrupt:
        log.debug("Controller exits")
    finally:
        log.debug("Exit")
        agent.stop()
