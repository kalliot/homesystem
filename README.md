# homesystem
mqtt related home controlling systems

Most of sensors are connected to esp32, it's the sensors repository, not under this project, but one level backwards.
This repository has only python codes, which run in linux machines. I have two raspberry pi:s.

dbsavers - programs to save data to an influx database
 
 consumption: data coming from sensors esp. Several temperatures, oil burner magnetic switch state and relay states.
 
 elconsumption: This is not in use anymore. Previously I read electricity consumption from houses electricity meter 
 led flashes. This is ok, if I had no solarpanels. Problems arise, when you have to know the direction of grid flow.
 
 elpower: Save the data from Shelly 3EM. Each phase is stored, as well as the sum of all phases. There is also an interesting parameter
 named as W15min. This a quality of quarterly consumed/produced energy.
 
 roomsensors
 
 savebattery
 
 savebosch
 
 saveprices
 
 savesolis
 
 saveweather


logic - as name says, has some kind of logics. Most clever of those controls a relay depending of
 electricity stock price.
 
opendata_readers - read data from weather service, solarpanel cloud and nordpool electricity stock. 

