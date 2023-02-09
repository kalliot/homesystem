import time
from datetime import datetime
from datetime import timezone
import json
import paho.mqtt.client as mqtt 
import paho.mqtt.subscribe as subscribe
from queue import Queue
import sys

sys.path.insert(1, '../config')
from influx_credentials import *

shellynumber = 1

class relay:
    def __init__(self, index, state, ts, energy):
        self.index = index
        self.state = state
        self.ts = ts
        self.initdone = False
        self.energy = energy

#relays = []
relays = [relay(0, False, 0, 0.0),
          relay(1, False, 0, 0.0),
          relay(2, False, 0, 0.0),
          relay(3, False, 0, 0.0)]

def publishRelay(num, state):
    relaymsg = {
        'id': 'relay',
        'device' : 'shelly' + str(shellynumber),
        'contact': num,
        'state': state
    }
    setrelaytopic="home/kallio/relay/" +str(num) +"/shelly"+ str(shellynumber) + "/state"
    client.publish(setrelaytopic,json.dumps(relaymsg),qos=0, retain=True)
    print("publishing", setrelaytopic, relaymsg)

def setRelay(num, state):
    global shellynumber

    relaymsg = {
        'id': 20,
        'src':'home/kallio/relayreply',
        'method':'Switch.Set',
        'params': {
                'id':num,
                'on':state
            }
    }
    setrelaytopic="shelly" + str(shellynumber) + "/rpc"
    client.publish(setrelaytopic,json.dumps(relaymsg))


def processData(eldata):
    global relays

    # {"src":"shellypro4pm-30c6f784e78c","dst":"shelly1/events","method":"NotifyStatus","params":
    # {"ts":1675072985.86,"switch:1":{"id":1,"apower":0,"current":0,"output":false,"pf":0,"source":"UI"}}}    

    # releen nappia painettiin, tilaksi tuli "on"
    #shelly1/events/rpc {"src":"shellypro4pm-30c6f784e78c","dst":"shelly1/events","method":"NotifyStatus","params":{"ts":1675931140.21,"switch:0":{"id":0,"output":true,"source":"UI"}}}

    # statistiikka
    # shelly1/events/rpc {"src":"shellypro4pm-30c6f784e78c","dst":"shelly1/events","method":"NotifyStatus","params":{"ts":1675935540.54,"switch:3":{"id":3,"aenergy":{"by_minute":[0.000,0.000,0.000],"minute_ts":1675935539,"total":0.000}}}}

    if not (eldata.get('id') is None):
        if (eldata['id'] == 'relay'):
            contact = eldata['contact']
            newstate = eldata['state']
            if relays[contact].state != newstate or relays[contact].initdone == False:
                relays[contact].initdone = True
                setRelay(contact, newstate)

    if not (eldata.get('method') is None):
        method = eldata['method']
        if method == 'NotifyStatus':
            params = eldata['params']
            ts = int(params['ts'])
            i=0
            while i < 4:
                swname = 'switch:' + str(i)
                if not (params.get(swname) is None):
                    relaydata =  params[swname]
                    if not (relaydata.get('output') is None):
                        state = relaydata['output']
                        if state != relays[i].state or relays[i].initdone == False:
                            print(i,"changed")
                            relays[i].initdone = True
                            relays[i].index = i
                            relays[i].state = state
                            relays[i].ts = ts
                            publishRelay(i, state)    
                    if not (relaydata.get('aenergy') is None):   
                        energy = relaydata['aenergy']      
                        relays[i].energy = float(energy['total'])
                        relays[i].ts = int(energy['minute_ts'])

                i = i + 1    
            for obj in relays:
                print(obj.index, obj.state, obj.ts, obj.energy, sep='-')    


def on_message(client, userdata, message):
    msgqueue.put(message.payload)


def on_connect(client, userdata, flags, rc):
    global connected
    if (rc==0):
        connected = True
    else:
        print("connection failed, rc=",rc)            
        connected = False

def on_disconnect(client, userdata, rc):
    client.reconnect()

def on_publish(client, userdata,result):
    pass


msgqueue = Queue(maxsize=10)


client = mqtt.Client("shelly" + str(shellynumber)) 
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.on_disconnect = on_disconnect
client.connect(mqtt_broker.address,port = mqtt_broker.port, keepalive=60) 
print(datetime.utcnow(), "Start")
client.loop_start()


topics = [("home/kallio/relay/shelly" + str(shellynumber) + "/setstate",0),
          ("shelly1/events/rpc",0)]
client.subscribe(topics)

while True:
    try:
        data = msgqueue.get(block=True)
        if data is None:
            continue
        processData(json.loads(data))
    except KeyboardInterrupt:
        client.disconnect()
        exit(0)
    except:
        raise        