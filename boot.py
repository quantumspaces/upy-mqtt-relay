"""Boot code of MQTT relay switch. Simply connects Wifi"""

import network
import machine
import config

def connect_wifi():
    """Await connection to WIFI"""

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Connecting to ", config.WIFI_SSID, end="")
    wlan.connect(config.WIFI_SSID, config.WIFI_PASS) 
    
    while not wlan.isconnected():
        print(".", end="")
        machine.idle() 
        
    print()
    print("Connected to ", config.WIFI_SSID) 
    print(wlan.ifconfig())

connect_wifi()
