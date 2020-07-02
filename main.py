"""Main module of MQTT relay switch"""

import machine
import ujson 
import time

from mqtt import MQTTClient 
import config
import relay_button

def subscribe_commands(topic, msg):
    """Callback function to handle messages on specific topic"""

    try:
        values = ujson.loads(msg)
        send_relay_command(values["bid"], values["on"])
    except ValueError as e:
        print("Malformed message - ", msg, "(topic", topic, "). Ignoring")

def connect_mqtt():
    """Connect to MQTT server and subscribe to command topics"""

    client = MQTTClient(config.MQTT_CLIENT, config.MQTT_SERVER, user="", password="", port=config.MQTT_PORT) 
    client.set_callback(subscribe_commands) 
    client.connect()
    print("Connected MQTT server at {}:{}".format(config.MQTT_SERVER, config.MQTT_PORT))
    client.subscribe(topic=config.TOPIC_COMMANDS) 
    print("Listening on topic '{}'".format(config.TOPIC_COMMANDS))
    return client

def restart_and_reconnect():
    """On failure, reboot the machine to start fresh"""
    
    print('Failed to connect to MQTT broker. Reconnecting ...')
    time.sleep(5)
    machine.reset()

def init_relay_buttons():
    """return array of buttons used"""

    rv = list()

    for i in range(4):
        rb = relay_button.RelayButton(i+1, config.RELAY_PINS[i], 0)
        rv.append(rb)
    
    return rv

def send_relay_command(relay_id, on_command):
    """Send the command to appropriate relay. If relay id is 0, send to all"""

    if relay_id == 0:
        for relay in relays:
            relay.button_push(on_command)
    else:
        for relay in relays:
            if relay_id == relay.button_id:
                relay.button_push(on_command)

def publish_status():
    """Publish status of all relays to the notification topic. Send this as a callback to
    each relay"""

    # TODO
    # for relay in relays:
    pass

# init relay array
relays = init_relay_buttons()

try:
    client = connect_mqtt()
except OSError as e:
    restart_and_reconnect()

while True:  
    try:
        client.check_msg()
        machine.idle()
        for relay in relays:
            relay.idle()
    except OSError as e:
        restart_and_reconnect()
