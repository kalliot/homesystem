# homesystem
mqtt related home controlling systems

Most of sensors are connected to esp32, it's the sensors repository, not under this project, but one level backwards.
This repository has only python codes, which run in linux machines. I have two raspberry pi:s.

****- dbsavers**** = programs to save data to an influx database. All the data is in mqtt topics, so I dont save to db 
 directly, instead first to mqtt topics and after that to db. 
 
 + consumption: data coming from sensors esp. Several temperatures, oil burner magnetic switch state and relay states.
 + elconsumption: This is not in use anymore. Previously I read electricity consumption from houses electricity meter 
 led flashes. This is ok, if I had no solarpanels. Problems arise, when you have to know the direction of grid flow.
 + elpower: Save the data from Shelly 3EM. Each phase is stored, as well as the sum of all phases. There is also an interesting parameter
 named as W15min. This a quality of quarterly consumed/produced energy.
 + roomsensors: These are a battery powered zigbee temperature/humidity sensors. I use SONOFF SNZB-02D sensors via SONOFF EFR32MG21
   zigbee dongle. The router software is zigbee2mqtt.
 + savebattery: saves the states of a raspberry pi ups board.
 + savebosch: bosch air to water heatpump data. I collect the data with bbqkees-electronics data collection dongle. The dongle is
   configured to send all data in one packet (not in home-assistang format).
 + saveprices: all electricity stock prices data are collected to mqtt topics, and this programs saves the data from topics to db.
 + savesolis: My Solis solar inverter data. 
 + saveweather: Weather forecast is in mqtt topics save way as electricity prices are.


****- logic**** = as name says, has some kind of logics. Most clever of those is maybe setrelay. 
 + bridge: reads a subset of my mqtt topics and relays a mqtt message to a public cloud. This is to monitor
   what's happening at home, when I am somewhere far away.
 + button: Very simple gpio reader for raspberry pi. When button is pressed, a mqtt message is sent. When button
   is released, send a new message.
 + button2relay: glue the button with one relay. This is done by reading buttontopic and relaytopic and sending to relay topic.
   If relay is on, show it with a led on raspberry pi. Note that the led is not dependent of button state, instead the relay state.
   This means that if relay state is changed with some other way than button press, the led is still in sync.
 + heatpump
 + phaserestrictor
 + setcurrentprice: tiny cron prog, which updates current price topic, data is taken from other price topics.
 + setcurrentvalues: shell script around setcurrent* pythons. This should be called just after the hour has been changed.
 + setcurrentweather: tiny cron prog, which updates current weather topic, data is taken from other weather topics.
 + setrelay: quite comples program, controlling my heating boiler according to stock electricity price and solar produced energy.
 + setupstorage:  Very simple program, saving my heating system setup to a file, when the topic is updated. In startup, the setup
   is read from disk and is sent to the topic. This program is not needed, if your mqtt gateway stores each topic to disk, so the
   topics are read from disk at bootup. I need only this topic, so i configure mosquitto not to save topics and so I need this prog.
 + shelly1
 + shelly4
 + shellyem
 + status
 + statusandups
 + 
****- opendata_readers**** - read data from weather service, solarpanel cloud and nordpool electricity stock.
 + getprices
 + getsolar
 + getweather

