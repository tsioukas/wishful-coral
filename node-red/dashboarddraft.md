## Coral Dashboard
- [Introduction](#intro)
	- [Instalation](#dashboardinstall)
	- [Connection](#tcpconnection)
- [DashBoard](#dashboard)
	- [Routing Algorithm](#routingalgorithm)
	- [Data Export](#dataexport)
	- [Experiment Replay](#experimentreplay)
- [RPL - Routing protocol for Low-Power and Lossy Networks](#rpl)
	- [Configuration](#rplconfiguration)
	- [Configuration Overview](#rplconfigoverview)
	- [Chart Data](#rpldata)
- [BCP - Backpressure routing protocol](#bcp)
	- [Configuration](#bcpconfiguration)
	- [Configuration Overview](#bcpconfigoverview)
	- [Chart Data](#bcpdata)
- [SDN - Software Defined Wireless Sensor Network routing protocol](#sdn)
	- [Actions](#sndcommands)
	- [Messages](#sdnmessages)
	- [Chart Data](#sdndata)
- [Common Incomming Data](#commondata)
	- [Network Setup](#networksetup)
	- [Monitoring Information](#monitoringinformation)
- [Topology Visualization](#topvis)
	- [Topology Data](#topvisdata)
	- [Commands](#topviscommands)
- [Topology Visualization Map](#topvismap)
<a name="intro" class="anchor" href="#intro"></a>
## Introduction

TODO : ?

<a name="dashboardinstall" class="anchor" href="#dashboardinstall"></a>
### Instalation

TODO : ?

<a name="tcpconnection" class="anchor" href="#tcpconnection"></a>
### Connection

TODO : HOW TO CONNECT

------------

<a name="dashboard" class="anchor" href="#dashboard"></a>
## DashBoard

<a name="routingalgorithm" class="anchor" href="#routingalgorithm"></a>
### Routing Algorithm

TODO : GENERAL

------------

<a name="dataexport" class="anchor" href="#dataexport"></a>
### Data Export

TODO : GET FROM FINAL

------------

<a name="experimentreplay" class="anchor" href="#experimentreplay"></a>
### Experiment Replay

TODO : GET FROM FINAL

----------
<a name="rpl" class="anchor" href="#rpl"></a>
## RPL - Routing protocol for Low-Power and Lossy Networks

<a name="rplconfiguration" class="anchor" href="#rplconfiguration"></a>
### Configuration

In this section we describe all the commands & configuration options from RPL Dashboard send to Controler.

The general format of JSON for all configuration options is this :
```json
{
    "RTA":"RPL",
    "CMD":"COMMAND",
    "NID":1,
    "VAL":1
}
```

- **RTA** : The Routing Algorithm. Always "RPL" for this protocol.
- **CMD** : The name of command
- **NID** : Node ID as defined on Nodes panel.
- **VAL** : The selected value of each option

#### Nodes

In panel nodes we define the target node of configuration properties. Possible values and their returns of node target are :

- **All** : Return 1000
- **SINK** : Return 1
- **Node** : Return the number on Node field

#### RPL DIO Interval Doublings

```json
{"RTA":"RPL", "CMD": "IEEE802154_RPL_Doublings", "NID": 1, "VAL": 8}
```

- **CMD** : "IEEE802154_RPL_Doublings"
- **VAL** : Range 8-13

#### RPL DIO Interval Min

```json
{"RTA":"RPL", "CMD": "IEEE802154_RPL_Imin", "NID": 1, "VAL": 8}
```

- **CMD** : "IEEE802154_RPL_Imin"
- **VAL** : Range 8-13


#### UDP send freq

```json
{"RTA":"RPL", "CMD": "CORAL_send_interval", "NID": 1, "VAL": 1}
```

- **CMD** : "CORAL_send_interval"
- **VAL** : Range 1-10

#### Link Quality Estimation Algorithm

```json
{"RTA":"RPL", "CMD": "LQEA", "NID": 1, "VAL": 1}
```

- **CMD** : "LQEA"
- **VAL** : 
-- **0** : "0F - Objective Function"
-- **1** : "ETX - Objective Function"


<a name="rplconfigoverview" class="anchor" href="#rplconfigoverview"></a>
### Configuration Overview

In this section we describe how to update the available information on Configuration Overview.

The general format of JSON for all configuration options is this :
```json
{
    "RTA":"RPL",
    "DTP":"CNF",
    "CMD":"COMMAND",
    "NID":1,
    "VAL":1
}
```

- **RTA** : The Routing Algorithm. Always "RPL" for this protocol.
- **DTP** : Defines the target using a data type. Always "CNF" for configuration overview
- **CMD** : The name of command
- **NID** : The Node ID of property
- **VAL** : The current value of configuration property

#### RPL DIO Interval Min


```json
{"RTA":"RPL", "DTP":"CNF","CMD":"IEEE802154_RPL_Imin","NID":1,"VAL":8}
```

- **CMD** : "IEEE802154_RPL_Imin"


#### RPL DIO Interval Doublings

```json
{"RTA":"RPL", "DTP":"CNF", "CMD":"IEEE802154_RPL_Doublings", "NID": 1, "VAL": 8}
```

- **CMD** : "IEEE802154_RPL_Doublings"

#### UDP send freq

```json
{"RTA":"RPL", "DTP":"CNF", "CMD":"CORAL_send_interval", "NID": 1, "VAL": 1}
```

- **CMD** : "CORAL_send_interval"

#### Link Quality Estimation Algorithm

```json
{"RTA":"RPL", "DTP":"CNF", "CMD":"LQEA", "NID": 1, "VAL": 1}
```

- **CMD** : "LQEA"

#### Note

> - If Node ID parameter is 1000 then all nodes receive the same value as was defined on Configuration Overview
> - If we give in any parameter the value “null” then removes corresponding configuration from list


<a name="rpldata" class="anchor" href="#rpldata"></a>
### Chart Data

In this section we describe the incoming data for each chart on RPL Dashboard.

The general format of JSON for all chart data is :

```json
{
    "RTA":"RPL",
    "DTP":"CHA",
    "CMD":"COMMAND",
    "NID":1,
    "VAL":1,
    "TIME":1483228800000
}
```


- **RTA** : The Routing Algorithm. Always "RPL" for this protocol.
- **DTP** : Defines the target using a data type. Always "CHA" for charts.
- **CMD** : Defines data property
- **NID** : The Node ID of propertiy
 - **VAL** : The value of property
- **TIME** : The timestamp of value in milliseconds

#### Packet Delivery Ratio (PDR)

```json
{"RTA":"RPL","DTP":"CHA","CMD":"CORAL_pdr_total_sink","NID":1, "VAL":0,"TIME":1483228800000}
```

- **CMD** : Defines data property
-- "CORAL_pdr_total_sink"
- **NID** : NodeID must be always 1

#### Control Packets vs. Data Packets

```json
{"RTA":"RPL","DTP":"CHA","CMD":"CORAL_icmp_send_total_sink","TIME":1483228800000,"VAL":0}
{"RTA":"RPL","DTP":"CHA","CMD":"CORAL_udp_send_total_sink","TIME":1483228800000,"VAL":0}
```
- **CMD** : Defines data property
-- "CORAL_icmp_send_total_sink" : Total Control Packets Sent
-- "CORAL_udp_send_total_sink" : Total UDP Packets Sent

#### Control Packets vs. Data Packets %

```json
{"RTA":"RPL","DTP":"CHA","CMD":"CORAL_udp_vs_control","TIME":1483228800000,"VAL": 0}
```
- **CMD** : Defines data property
-- "CORAL_icmp_send_total_sink" : Total Control Packets Sent
-- "CORAL_udp_send_total_sink" : Total UDP Packets Sent

#### Node Jitter

```json
{"RTA":"RPL", "DTP":"CHA","CMD": "jitter", "TIME": 1483228800000, "NID": 2, "VAL": 0 }
```
- **CMD** : Defines data property
-- "CORAL_pdr_total_sink"
- **NID** : Node ID

#### Jitter Average

```json
{"RTA":"RPL", "DTP":"CHA","CMD": "jitter", "TIME": 1483228800000, "NID": 1000, "VAL": 0 }
```
- **CMD** : Defines data property
-- "jitter"
- **NID** : When NodeID is 1000, then defined the average value.

#### Latency

```json
{"RTA":"RPL", "CMD": "CORAL_latency", "TIME": 1483228800000, "NID": 1000, "VAL": 0 }
```
- **CMD** : Defines data property
-- "CORAL_latency"
- **NID** : Always 1000

----------
<a name="bcp" class="anchor" href="#bcp"></a>
## BCP - Backpressure routing protocol

<a name="bcpconfiguration" class="anchor" href="#bcpconfiguration"></a>
### Configuration

In this section we describe all the commands & configuration options from BCP Dashboard send to Controler.

The general format of JSON for all configuration options is this :
```json
{
    "RTA":"BCP",
    "CMD":"COMMAND",
    "NID":1,
    "VAL":1
}
```

- **RTA** : The Routing Algorithm. Always "BCP" for this protocol.
- **CMD** : The name of command
- **NID** : Node ID as defined on Nodes panel.
- **VAL** : The selected value of each option

#### Nodes

In panel nodes we define the target node of configuration properties. Possible values and their returns of node target are :

- **All** : Return 1000
- **SINK** : Return 1
- **Node** : Return the number on Node field

#### Weights

```json
{"RTA":"BCP", "CMD": "WEIGHT", "NID": 0, "VAL": 0}
```

- **CMD** : "WEIGHT"
- **VAL** : Range 0-50

#### Queue Limits
```json
{"RTA":"BCP", "CMD": "QUEUELIMIT", "NID": 0, "VAL": 0}
```

- **CMD** : "QUEUELIMIT"
- **VAL** : Range 0-50

#### Data Packet send freq (sec)

```json
{"RTA":"BCP", "CMD": "DATAPACKETFREQ", "NID": 0, "VAL": 0}
```

- **CMD** : "DATAPACKETFREQ"
- **VAL** : Range 1-120

<a name="bcpconfigoverview" class="anchor" href="#bcpconfigoverview"></a>
### Configuration Overview

In this section we describe how to update the available information on Configuration Overview.

The general format of JSON for all configuration options is this :
```json
{
    "RTA":"BCP",
    "DTP":"CNF",
    "CMD":"COMMAND",
    "NID":1,
    "VAL":1
}
```

- **RTA** : The Routing Algorithm. Always "BCP" for this protocol.
- **DTP** : Defines the target using a data type. Always "CNF" for configuration overview
- **CMD** : The name of command
- **NID** : The Node ID of property
- **VAL** : The current value of configuration property


#### Weights

```json
{"RTA":"BCP", "DTP":"CNF", "CMD":"WEIGHT", "NID": 1, "VAL": 1}
```
- **CMD** : "WEIGHT"

#### Queue Limits

```json
{"RTA":"BCP", "DTP":"CNF", "CMD":"QUEUELIMIT", "NID": 1, "VAL": 1}
```
- **CMD** : "QUEUELIMIT"

#### Data Packet send freq (sec)

```json
{"RTA":"BCP", "DTP":"CNF", "CMD":"DATAPACKETFREQ", "NID": 1, "VAL": 1}
```
- **CMD** : "QUEUELIMIT"

#### Note

> - If Node ID parameter is 1000 then all nodes receive the same value as was defined on Configuration Overview
> - If we give in any parameter the value “null” then removes corresponding configuration from list


<a name="bcpdata" class="anchor" href="#bcpdata"></a>
### Chart Data

In this section we describe the incoming data for each chart on RPL Dashboard.

The general format of JSON for all chart data is :

```json
{
    "RTA":"BCP",
    "DTP":"CHA",
    "CMD":"COMMAND",
    "NID":1,
    "VAL":1,
    "TIME":1483228800000
}
```

- **RTA** : The Routing Algorithm. Always "BCP" for this protocol.
- **DTP** : Defines the target using a data type. Always "CHA" for charts.
- **CMD** : Defines data property
- **NID** : The Node ID of propertiy
 - **VAL** : The value of property
- **TIME** : The timestamp of value in milliseconds


#### Packets in Queues

```json
{"RTA":"BCP","DTP":"CHA","CMD":"PACKETSQUEUES","NID":1,"VAL": 0}
```

- **CMD** : "PACKETSQUEUES"


----------
<a name="sdn" class="anchor" href="#sdn"></a>
## SDN - Software Defined Wireless Sensor Network routing protocol


<a name="sndcommands" class="anchor" href="#sdncommands"></a>
### Actions

In this section we describe all the commands & configuration options from SDN Dashboard send to Controller.

#### Start & Update

TODO : What it does

```json
{"RTA":"SDN","CMD":"Start","SINK":"01.00","TCT":0,"ACK":0,"RET":0,"ROUT":0,"LQEA":0}
{"RTA":"SDN","CMD":"Update","SINK":"01.00","TCT":0,"ACK":0,"RET":0,"ROUT":0,"LQEA":0}
```

- **RTA** : The Routing Algorithm. Always "SDN" for this protocol.
- **CMD** : The name of command
-- "Start" : To start a new experiment
-- "Update" : To update configuration
- **SINK** : The value of SINK ID field
- **TCT** :
 -- 0 : Topology control advertisement based
 -- 1 : Topology control node neighbors list based
- **ACK** : 
-- 0 : Topology control without Acknowledgement
-- 1 : Topology control with Acknowledgement
- **RET** : The value of  Retransmission delay field. Range 1-10
- **ROUT** : The value of  Routing Configuration field
-- 0 : Next hop only
-- 1 : Total Path
- **LQEA** : The value of  Link Quality Estimation field
-- 0 : RSSI
-- 1 : RSSI & Energy
-- 2 : ΕΤΧ
-- 3 : JSI intelligent LQE algorithm

#### Clear Routes

TODO : What it does

```json
{"RTA":"SDN","CMD":"ClearRoutes"}
```
- **RTA** : The Routing Algorithm. Always "SDN" for this protocol.
- **CMD** : Takes value of "ClearRoutes"

#### Save

TODO : What it does

```json
{"RTA":"SDN","CMD":"Save","FILE":"EXPERIMENTTITLE"}
```
- **RTA** : The Routing Algorithm. Always "SDN" for this protocol.
- **CMD** : Takes value of "ClearRoutes"
- **FILE** : The value of Experiment Title field

#### Stop/Clear

TODO : What it does

```json
{"RTA":"SDN","CMD":"Clear"}
```
- **RTA** : The Routing Algorithm. Always "SDN" for this protocol.
- **CMD** : Takes value of "Clear"

<a name="sdnmessages" class="anchor" href="#sdnmessages"></a>
### Messages

Messages panel can display log messages from controller. 

```json
{"RTA":"SDN","DTP":"LOG", "TIME":1483228800000, "MSG":"MESSAGE TEXT"}
```

- **RTA** : The Routing Algorithm. Always "SDN" for this protocol.
- **DTP** : Defines the target using a data type. Always "LOG" for messages.
- **MSG** : The content of message
- **TIME** : The timestamp of value in milliseconds. This is an optional value, if TIME not defined on JSON, current local timestamp will used.

<a name="sdndata" class="anchor" href="#sdndata"></a>
### Chart Data

In this section we describe the incoming data for each chart on SDN Dashboard.

The general format of JSON for all chart data is :

```json
{
    "RTA":"SDN",
    "DTP":"CHA",
    "CMD":"COMMAND",
    "NID":1,
    "VAL":1,
    "TIME":1483228800000
}
```

- **RTA** : The Routing Algorithm. Always "SDN" for this protocol.
- **DTP** : Defines the target using a data type. Always "CHA" for charts.
- **CMD** : Defines data property
- **NID** : The Node ID of propertiy
 - **VAL** : The value of property
- **TIME** : The timestamp of value in milliseconds


TODO : Change IN DASHBOARD/CONTROLLER "DTP" TO "CMD". SET "DTP" AS "CHA"

#### Topology Discovery time elapsed

```json
{"RTA":"SDN","DTP":"CHA","CMD":"TOPDISTE","TIME":1483228800000,"NODES": 0}
```

- **CMD** : "TOPDISTE"
- **TIME** : Time in milliseconds
- **NODES** : Number of Nodes


#### Topology Discovery Control Packets

```json
{"RTA":"SDN","DTP":"CHA","CMD":"TOPDISCP","TIME":1483228800000,"SENT": 10,"RECV": 20,"TOTAL": 30}

```

- **CMD** : "TOPDISTE"
- **TIME** : Time in milliseconds
- **SENT** : Packets Sent
- **SENT** :  Packets Received
- **TOTAL** :  Total Packets

#### First Packet delivery

```json
{"RTA":"SDN","DTP":"CHA","CMD":"FRPCKDL","TIME":1000,"NID": 1}
```

- **CMD** : "FRPCKDL"
- **TIME** : Time in milliseconds
- **NID** : Node ID

----------
<a name="commondata" class="anchor" href="#commondata"></a>
## Common Incomming Data

Network Setup and Monitoring Information are some common features on each protocol. In this section will describe how controler send these informations to dashboard with incoming JSON command.

------------

<a name="networksetup" class="anchor" href="#networksetup"></a>
### Network Setup

#### Network Definition

This command changes the network information on dashboard.

```json
{"RTA":"RPL","DTP":"NET","NODES":10,"SINK":1,"STATIC":5,"MOBILE":4,"LINKS":10}
```
- **RTA** : Routing Algorithm. The values can be "RPL", "SDN" & "BCP"
- **DTP** : Data Type
- **NODES** : The number of network nodes
- **SINK** : The number of SINK nodes
- **STATIC** : The number of static nodes
- **MOBILE** : The number of mobile nodes
- **LINKS** : The number of links between nodes

#### Reset Network

This command remove any network information on dashboard and set it on initial state.

```json
{"RTA":"RPL","DTP":"NET","NODES":0,"SINK":0,"STATIC":0,"MOBILE":0}
```

#### Additional functions

It is possible to change only a part of the Network:

```json
{"RTA":"RPL","DTP":"NET","STATIC":4,"MOBILE":6}
```

------------

### Monitoring Information

With these commands will set the time that elapsed on our experiment. This time can be set only one time at the start of the session. Optionaly can periodicaly updated to calibrate the time.

The are two types of calculation

#### Base on the duration of the experiment

This command will set the current duration of the experiment. System will calculate the time that elapsed from that time and will display it on the panel.

```json
{"RTA":"RPL","DTP":"MON","DURATION":60000}
```

- **RTA** : Routing Algorithm. The values can be "RPL", "SDN" & "BCP"
- **DTP** : Data Type
- **DURATION** : The duration of implementation of experiment in milliseconds.

#### Base on a specific unix timestamp

```json
{"RTA":"RPL","DTP":"MON","STARTTIME":1483228800000}
```

- **RTA** : Routing Algorithm. The values can be "RPL", "SDN" & "BCP"
- **DTP** : Data Type
- **STARTTIME** : The start of implementation of experiment in unix timestamp. e.g 148322880000 = Sun, 01 Jan 2017 00:00:00 GMT

#### Additional functions

```json
{"RTA":"RPL","DTP":"MON","ACTION":"START"}
```

- **RTA** : Routing Algorithm. The values can be "RPL", "SDN" & "BCP"
- **DTP** : Data Type
- **START** : Continues the timer based on the latest value. No need to rerun every time when a new DURATION or STARTTIME value arrives or in case the time enters in START condition.

```json
{"RTA":"RPL","DTP":"MON","ACTION":"STOP"}
```
- **RTA** : Routing Algorithm. The values can be "RPL", "SDN" & "BCP"
- **DTP** : Data Type
- **STOP** : In this case the timer does not present. With START condition, it continues with base the running value (it does not function as PAUSE)

----------
<a name="topvis" class="anchor" href="#topvis"></a>
## Topology Visualization

In this section we will describe the topology visuliation data structure, that used on SDN routing algorithm

There are two kind of data that can send in this Node Red module

- Topology Data (Nodes, Links and Flows)
- Topology Map

<a name="topvisdata" class="anchor" href="#topvisdata"></a>
### Topology Data

Topology Visualization accepts the data in json format. This data stucture include information's about topology Nodes, Links and Flows.

#### Data Structure
A general format of topology data structure can be this example :

```json
{
	"RTA":"SDN",
	"DTP":"TOP",
    "nodes": [
        {
            "id": "00.00",
            "type": 1,
            "title": "Controler",
            "class": "controler",
            "realX": 0,
            "realY": 0, 
            "data": {
                "description": "Network Controler",
                "energy": 5,
                "any kind of data": 10
            }
        },
        {
            "id": "01.00",
            "type": 2,
            "realX": 100,
            "realY": 0, 
            "data": {
                "description": "Sink 01.00",
                "energy": 4
            }
        },
        {
            "id": "02.00",
            "type": 2,
            "realX": 100,
            "realY": 100, 
            "data": {
                "description": "Node 02.00",
                "energy": 3
            }
        }   
    ],
    "links": [
        {
            "source": "00.00",
            "target": "01.00",
            "data": {
                "RSSI_R":60,
                "RSSI_S":62
            }
        },
        {
            "source": "01.00",
            "target": "02.00",
            "data": {
                "RSSI_R":60,
                "RSSI_S":62
            }
        }
    ],
    "flows": [
        {
            "color": "yellow",            
            "links": [
                { 
                    "source": "00.00",
                    "target": "01.00"
                },
                { 
                    "source": "01.00",
                    "target": "02.00"
                }
            ]
        }
    ]
}
```
- **RTA** : The Routing Algorithm. Available options are "RSI", "BCA", "SDN".
- **DTP** : Defines the target using a data type. Always "TOP" for topology visualization.
- **nodes** :  Array of nodes and their information. If there are no changes in node structure and data, it's not necessary to resend the node data. The array structure contains for each node these properties :
	- **id** : The unique ID of node. Used for reference on links and flows.
	- **type** : The type of node. At this time there are two options available. Also this option set the icon of the node.
		- 1 :  Controller
		- 2 :  Node
	- **title** : Optionally the title of node.
	- **class** :  This is optional and set the CSS class of node for further styling
	- **realX / realY** : Optionally if the node has a known position realX and realY defines this cordinates.
		- When a topology map loaded then the system will convert these position to our map scale.
		- If map isn't loaded it will set automatic to scale 1 and the unit will calculated as 1 pixel.
		- If realX and realY isn't defined then topology visualization will calculate automatic the coordinates.
	- **data** :  An array of node properties. These information's displayed as popup on mouse over.
- **links** :  A list of links between nodes
	- **source** : The source node id
	- **target** : The target node id
	- **data** : An array of link properties. These information's displayed as popup on mouse over. Key of property will used as label.
- **flows** : This contains an array of the path of flows. This is an optional if there is no flows in the topology. Also you can send only the flows without nodes and links. To remove flows send an empty array.
	- **color** : An optional property that defines the color of the flow. Below you can find color names and their id's. It's possible to set the number of the name of the color. If the color didn't defined then it will used an automatic color .
	- **links** : An array of flow links.  It descibes each step of the full path between connected nodes
		- **source** : The source node id
		- **target** : The target node id

#### Flow Colors

Below is the list of possible flow colors. These colors based on google material design palette.

```json
{"1":"red","2":"pink","3":"purple","4":"deep-purple","5":"indigo","6":"blue","7":"light-blue","8":"cyan","9":"teal","10":"green","11":"light-green","12":"lime","13":"yellow","14":"amber","15":"orange","16":"deep-orange","17":"brown","18":"grey","19":"blue-grey"}
```

<a name="topviscommands" class="anchor" href="#topviscommands"></a>
### Commands

In this section we describe the returning commands of topology visualization.

There are some common options on each command.

- **RTA** : The Routing Algorithm. Available options are "RSI", "BCA", "SDN".
- **CMD** : The name of command
- **NID** : Node ID as defined on Nodes panel.

#### Discover Neighbors

> TODO : DESCRIBE WHAT  IT DOES

```json
{"RTA":"SDN","CMD":"Topology","NID":"01.00"}
```
- **CMD** : Topology

#### Send Message

> TODO : DESCRIBE WHAT  IT DOES

```json
{"RTA":"SDN","CMD":"Message","NID":"01.00"}
```
- **CMD** : Message


<a name="topvismap" class="anchor" href="#topvismap"></a>
## Topology Visualization Map

In this section we describe the data structure of the Map feature of Topology Visualization. 

#### Data Structure

```json
{
    "RTA":"SDN",
    "DTP":"TOP",
    "cmd":"setMap",
    "topologyConfig":{
        "charge": -400,
        "gravity": 0.05,
        "distance": 60,
        "initScale": 1,
        "minScale": 0.1,
        "maxScale": 5,
        "nodeCircleSize": 18,
        "nodeImageSize" : 24,
        "nodeLabelDistance" : 2.2
    },
    "map": {
        "name": "Name of Map",
        "mapUnit":1,
        "realUnit":1
    },
    "canvas":{
        "x":0,
        "y":0,
        "width":1000,
        "height":1000,
        "gridSize":500,
        "gridSubDivisions":5
    },  
    "elementsStyle":{
        "elementname":{
            "cssoption": "cssvalue"
        }
    },
    "elements":[
        {
            "type":"rect",
            "name":"elementname",
            "class":"",
            "style":"",
            "x":0,
            "y":0,
            "width":100,
            "height":100,
            "label":""
        }
    ]
}
```

- **RTA** : The Routing Algorithm.
- **DTP** : Defines the target using a data type. Always "TOP" for topology visualization.
- **CMD** : Defines the data structure action. For MAP JSON is setMap.
- **topologyConfig** : A set of config options for Topology Visualization module.
	- **charge** : In automatic node position is the charge between nodes. See [D3.js Force Layout](https://github.com/d3/d3-3.x-api-reference/blob/master/Force-Layout.md#charge) for more information.
	- **gravity** : In automatic node position is the gravity between nodes. See [D3.js Force Layout](https://github.com/d3/d3-3.x-api-reference/blob/master/Force-Layout.md#gravity) for more information.
	- **distance** : In automatic node position the distance between nodes in pixels. See [D3.js Force Layout](https://github.com/d3/d3-3.x-api-reference/blob/master/Force-Layout.md#chargeDistance) for more information.
	- **initScale** :  Initial scale when map loaded
	- **minScale** : Minimum scale of map zoom
	- **maxScale** : Maximum scale of map zoom
	- **nodeCircleSize** : Size of node in pixels
	- **nodeImageSize** : Size of icon on node in pixels
	- **nodeLabelDistance** :
- **map** :
	- **name** : A name of our Map
	- **mapUnit** : This is the units in our visualization environment. Usually set it as 1 pixel.
	- **realUnit** : This is the real word units. I defines how many Map units is the number of Real unit option. 

- **canvas** : Draws a background grid
	- **x** :  The horizontal position of grid
	- **y** : The vertical position of grid
	- **width** : The width of grid
	- **height** : The height of grid
	- **gridSize** : Set the width and height of horitontal and vertical grid lines
	- **gridSubDivisions** : Set the number of sub divisions
- **elementsStyle** : An array with css properties for each element.
- **elements** : An array with the list of all elements in our Map.

#### Elements Style

Elements style contains CSS information about each element group. It's a simple Style Sheet and it's possible to use all SVG CSS formatting rules. 

An example of this JSON can be like this :

```json
    "elementsStyle":{
        "wall":{
            "fill": "red",
            "stroke": "black",
            "stroke-width": "1px"
        }
    }
```
Using the above code we set as background fill the color red, with 1px black stroke on all elements with name "wall" 

#### Elements Types

This array used to draw includes all objects in our map. The are 3 basic kind of SVG objects supported :

- Rectangles
- Lines
-  Circles

There are some common options on each element type

- **type** : The type of element
- **name** : The name of element that also used in element styles. More than one objects can have the same name.
- **class**: An extra css class for the specific object
- **style** : An extra style code for the specific element


#### Rectangles

Draws an rectangle in the map

```json
    "elements":[
        {
            "type":"rect",
            "name":"elementname",
            "class":"",
            "style":"",
            "x":0,
            "y":0,
            "width":100,
            "height":100,
            "label":""
        }
    ]
```

- **type** : For rectangle elements "rect"
- **x** : The horizontal coordinate of top left corner in the rectangle
- **y** : The vertical coordinate of top left corner in the rectangle
- **width** : The width of rectangle
- **height** : The height of the rectangle
- **label** : A text object in the middle of circle. As with rectangles, it's possible set font style and type of all elements with the same name using this selector in elements style "elementname-label".

#### Lines

Draws a line in the map

```json
    "elements":[
        {
            "type":"line",
            "name":"elementname",
            "class":"",
            "style":"",
            "x1":0,
            "y1":0,
            "x2":0,
            "y2":0
        }
    ]
```

- **type** : For line elements "line"
- **x1** : The first point horizontal coordinate of line
- **y1** : The first point vertical coordinate of line
- **x2** : The second point horizontal coordinate of line
- **y2** : The second point vertical coordinate of line

#### Circles

Draws a circle in the map

```json
    "elements":[
        {
            "type":"circle",
            "name":"elementname",
            "class":"",
            "style":"",
            "cx":0,
            "cy":0,
            "r":100,
            "label":""
        }
    ]
```

- **type** : For circle elements "circle"
- **cx** : The horizontal coordinate dinate of the middle of circle
- **cy** : The vertical coordinate of the middle of circle
- **r** : The radius of circle
- **label** : A text object in the middle of circle. As with circles, it's possible set font style and type of all elements with the same name using this selector in elements style "elementname-label".
