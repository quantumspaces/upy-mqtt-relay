"""module relay_button.py: Encapsulates functionality of one relay switching."""

from machine import Pin
import time

import config

class RelayButton():
    """encapsulates the button behavior"""

    def __init__(self, button_id, relay_pin, bypass_pin, button_mode=b"pulse"):

        self.button_id = button_id
        self.relay_pin = relay_pin # the pin controlling this button
        self.bypass_pin = bypass_pin # the pin awaiting pulses to bypass MQTT. Future
        self.button_mode = button_mode # define modes such as pulse, on-off, ...

        self.button_on = False

        # actual pin object. Internal
        self._rpin = Pin(self.relay_pin, Pin.OUT)
        self._rpin.value(0)

        # prepare button timer variables
        self._counting = False
        self._start_time = time.time()

    def button_push(self, on_command):
        """action called when button is pushed, based on event or bypass"""

        if not self.button_on:
            # start a new button push
            self.button_on = True
            self._rpin.value(1)
            # start counter. Primitive comparison, but effective
            self._start_time = time.time()
            self._counting = True
        else:
            # ignore message
            pass

    def _button_release(self):
        """Release button, called by timer"""

        self.button_on = False
        self._rpin.value(0)

    def idle(self):
        """Call this often. This counts time etc."""

        if self._counting:
            # compare timers to send a release signal
            if time.time() >= self._start_time + config.BUTTON_PULSE_TIMEOUT:
                # done
                self._counting = False
                self._button_release()
