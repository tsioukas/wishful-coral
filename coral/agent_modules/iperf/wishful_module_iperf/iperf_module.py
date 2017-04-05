import logging
import wishful_upis as upis
import wishful_framework as wishful_module

__author__ = "Piotr Gawlowicz, Mikolaj Chwalisz"
__copyright__ = "Copyright (c) 2015, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{gawlowicz, chwalisz}@tkn.tu-berlin.de"

'''
    Packet flows are generated using IPerf tool.
'''
@wishful_module.build_module
class IperfModule(wishful_module.AgentModule):
    def __init__(self):
        super(IperfModule, self).__init__()
        self.log = logging.getLogger('IperfModule.main')


    @wishful_module.bind_function(upis.net.create_packetflow_sink)
    def start_server(self, port):
        self.log.debug("Starts iperf server on port {}".format(port))

        return "Server_started"


    @wishful_module.bind_function(upis.net.destroy_packetflow_sink)
    def stop_server(self):
        self.log.debug("Stops iperf server.")

        return "Server_started"


    @wishful_module.bind_function(upis.net.start_packetflow)
    def start_packetflow(self, dest_ip, port):
        self.log.debug("Start iperf client.")

        return "Client started"


    @wishful_module.bind_function(upis.net.stop_packetflow)
    def stop_packetflow(self):
        self.log.debug("Stops iperf client.")

        return "Client stopped"

