# homesystem
mqtt related home controlling systems

Most of sensors are connected to esp32, it's the sensors repository, not under this project, but one level backwards.
This repository has only python codes, which run in linux machines. I have two raspberry pi:s.

dbsavers - programs to save data to an influx database
logic - as name says, has some kind of logics. Most clever of those controls a relay depending of
 electricity stock price.
opendata_readers - read data from weather service, solarpanel cloud and nordpool electricity stock. 

