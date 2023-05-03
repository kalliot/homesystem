
class influx:
    url="http://localhost:8086"
    bucket="home_2week"
    org="Kallio"
    token="<your influx generated token>"

class nordpool:
    BaseURL = 'https://api.spot-hinta.fi/TodayAndDayForward'

class mqtt_broker:
    address = "192.168.101.231"
    port = 1883

class weather:
    BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
    ApiKey='<your apikey for visualcrossing>'
    Location='nastola,finland'

class solis:
    key = "<solis cloud apikey>"
    secret = '<solis cloud secret>'
    userid = "<id in your solis cloud url>"
    serialnumber = "<your inverter serial number. It is visible as Inverter SN column in cloud view>"    