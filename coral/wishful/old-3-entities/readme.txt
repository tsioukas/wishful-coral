#run example controller
#run with -v for debugging
./wishful_simple_controller --config ./controller_config.yaml 

#run example agent
#run with -v for debugging
./wishful_simple_agent --config ./agent_config.yaml


ATTENTION:
Don't forget to install serial for python3
pip3 install pyserial

Otherwise the agent will not be able to read from serial
