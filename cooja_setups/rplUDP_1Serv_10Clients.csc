<?xml version="1.0" encoding="UTF-8"?>
<simconf>
  <project EXPORT="discard">[APPS_DIR]/mrm</project>
  <project EXPORT="discard">[APPS_DIR]/mspsim</project>
  <project EXPORT="discard">[APPS_DIR]/avrora</project>
  <project EXPORT="discard">[APPS_DIR]/serial_socket</project>
  <project EXPORT="discard">[APPS_DIR]/collect-view</project>
  <project EXPORT="discard">[APPS_DIR]/powertracker</project>
  <project EXPORT="discard">[APPS_DIR]/serial2pty</project>
  <project EXPORT="discard">[APPS_DIR]/mobility</project>
  <simulation>
    <title>My simulation</title>
    <speedlimit>1.0</speedlimit>
    <randomseed>123456</randomseed>
    <motedelay_us>1000000</motedelay_us>
    <radiomedium>
      org.contikios.cooja.radiomediums.UDGM
      <transmitting_range>50.0</transmitting_range>
      <interference_range>100.0</interference_range>
      <success_ratio_tx>1.0</success_ratio_tx>
      <success_ratio_rx>0.9</success_ratio_rx>
    </radiomedium>
    <events>
      <logoutput>940000</logoutput>
    </events>
    <motetype>
      org.contikios.cooja.mspmote.RM090MoteType
      <identifier>rm0901</identifier>
      <description>RM090 Mote Type #rm0901</description>
      <source EXPORT="discard">[CONTIKI_DIR]/examples/ipv6/rpl-udp/udp-server.c</source>
      <commands EXPORT="discard">make udp-server.rm090 TARGET=rm090</commands>
      <firmware EXPORT="copy">[CONTIKI_DIR]/examples/ipv6/rpl-udp/udp-server.rm090</firmware>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.RimeAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Mote2MoteRelations</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.MoteAttributes</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspClock</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspButton</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.CC2520Radio</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.UsciA1Serial</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspLED</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDebugOutput</moteinterface>
    </motetype>
    <motetype>
      org.contikios.cooja.mspmote.RM090MoteType
      <identifier>rm0902</identifier>
      <description>RM090 Mote Type #rm0902</description>
      <source EXPORT="discard">[CONTIKI_DIR]/examples/ipv6/rpl-udp/udp-client.c</source>
      <commands EXPORT="discard">make udp-client.rm090 TARGET=rm090</commands>
      <firmware EXPORT="copy">[CONTIKI_DIR]/examples/ipv6/rpl-udp/udp-client.rm090</firmware>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.RimeAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Mote2MoteRelations</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.MoteAttributes</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspClock</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspButton</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.CC2520Radio</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.UsciA1Serial</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspLED</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDebugOutput</moteinterface>
    </motetype>
    <motetype>
      org.contikios.cooja.mspmote.RM090MoteType
      <identifier>rm0903</identifier>
      <description>RM090 Mote Type #rm0903</description>
      <source EXPORT="discard">[CONTIKI_DIR]/examples/ipv6/rpl-udp/udp-client.c</source>
      <commands EXPORT="discard">make udp-client.rm090 TARGET=rm090</commands>
      <firmware EXPORT="copy">[CONTIKI_DIR]/examples/ipv6/rpl-udp/udp-client.rm090</firmware>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.RimeAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Mote2MoteRelations</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.MoteAttributes</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspClock</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspButton</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.CC2520Radio</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.UsciA1Serial</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspLED</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDebugOutput</moteinterface>
    </motetype>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>43.56256904118027</x>
        <y>56.678638118409985</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>1</id>
      </interface_config>
      <motetype_identifier>rm0901</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>29.28664959815664</x>
        <y>31.66731684872363</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>2</id>
      </interface_config>
      <motetype_identifier>rm0902</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>57.98496790520324</x>
        <y>43.2220712600505</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>3</id>
      </interface_config>
      <motetype_identifier>rm0902</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>78.52031318404643</x>
        <y>44.57861989035258</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>4</id>
      </interface_config>
      <motetype_identifier>rm0903</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>70.7278914638825</x>
        <y>18.1435357884567</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>5</id>
      </interface_config>
      <motetype_identifier>rm0903</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>67.94392901502829</x>
        <y>64.76520590783255</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>6</id>
      </interface_config>
      <motetype_identifier>rm0903</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>37.013479395391</x>
        <y>15.069154658849316</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>7</id>
      </interface_config>
      <motetype_identifier>rm0903</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>50.86329074275608</x>
        <y>25.762220053834355</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>8</id>
      </interface_config>
      <motetype_identifier>rm0903</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>64.36552141902426</x>
        <y>5.638134494605662</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>9</id>
      </interface_config>
      <motetype_identifier>rm0903</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>88.15282325852516</x>
        <y>22.171048821889492</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>10</id>
      </interface_config>
      <motetype_identifier>rm0903</motetype_identifier>
    </mote>
  </simulation>
  <plugin>
    org.contikios.cooja.plugins.SimControl
    <width>280</width>
    <z>0</z>
    <height>160</height>
    <location_x>400</location_x>
    <location_y>0</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Visualizer
    <plugin_config>
      <moterelations>true</moterelations>
      <skin>org.contikios.cooja.plugins.skins.IDVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.GridVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.TrafficVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.UDGMVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.MoteTypeVisualizerSkin</skin>
      <viewport>4.84626496284329 0.0 0.0 4.84626496284329 -106.73055324097058 25.40337907026708</viewport>
    </plugin_config>
    <width>400</width>
    <z>2</z>
    <height>400</height>
    <location_x>1</location_x>
    <location_y>1</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.LogListener
    <plugin_config>
      <filter />
      <formatted_time />
      <coloring />
    </plugin_config>
    <width>548</width>
    <z>1</z>
    <height>240</height>
    <location_x>186</location_x>
    <location_y>170</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.TimeLine
    <plugin_config>
      <mote>0</mote>
      <mote>1</mote>
      <mote>2</mote>
      <mote>3</mote>
      <mote>4</mote>
      <mote>5</mote>
      <mote>6</mote>
      <mote>7</mote>
      <mote>8</mote>
      <mote>9</mote>
      <showRadioRXTX />
      <showRadioHW />
      <showLEDs />
      <zoomfactor>500.0</zoomfactor>
    </plugin_config>
    <width>948</width>
    <z>-1</z>
    <height>166</height>
    <location_x>-225</location_x>
    <location_y>563</location_y>
    <minimized>true</minimized>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Notes
    <plugin_config>
      <notes>Enter notes here</notes>
      <decorations>true</decorations>
    </plugin_config>
    <width>268</width>
    <z>13</z>
    <height>160</height>
    <location_x>680</location_x>
    <location_y>0</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.Serial2Pty
    <mote_arg>0</mote_arg>
    <plugin_config />
    <width>250</width>
    <z>5</z>
    <height>100</height>
    <location_x>5</location_x>
    <location_y>418</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.Serial2Pty
    <mote_arg>1</mote_arg>
    <plugin_config />
    <width>250</width>
    <z>4</z>
    <height>100</height>
    <location_x>246</location_x>
    <location_y>409</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.Serial2Pty
    <mote_arg>2</mote_arg>
    <plugin_config />
    <width>250</width>
    <z>3</z>
    <height>100</height>
    <location_x>532</location_x>
    <location_y>410</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.Serial2Pty
    <mote_arg>3</mote_arg>
    <plugin_config />
    <width>250</width>
    <z>12</z>
    <height>100</height>
    <location_x>5</location_x>
    <location_y>520</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.Serial2Pty
    <mote_arg>4</mote_arg>
    <plugin_config />
    <width>250</width>
    <z>11</z>
    <height>100</height>
    <location_x>268</location_x>
    <location_y>513</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.Serial2Pty
    <mote_arg>5</mote_arg>
    <plugin_config />
    <width>250</width>
    <z>10</z>
    <height>100</height>
    <location_x>540</location_x>
    <location_y>515</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.Serial2Pty
    <mote_arg>6</mote_arg>
    <plugin_config />
    <width>250</width>
    <z>9</z>
    <height>100</height>
    <location_x>4</location_x>
    <location_y>623</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.Serial2Pty
    <mote_arg>7</mote_arg>
    <plugin_config />
    <width>250</width>
    <z>8</z>
    <height>100</height>
    <location_x>281</location_x>
    <location_y>615</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.Serial2Pty
    <mote_arg>8</mote_arg>
    <plugin_config />
    <width>250</width>
    <z>7</z>
    <height>100</height>
    <location_x>552</location_x>
    <location_y>618</location_y>
  </plugin>
  <plugin>
    de.fau.cooja.plugins.Serial2Pty
    <mote_arg>9</mote_arg>
    <plugin_config />
    <width>250</width>
    <z>6</z>
    <height>100</height>
    <location_x>-8</location_x>
    <location_y>741</location_y>
  </plugin>
</simconf>

