from switches.base import Switch

class PinSwitch(Switch):
    pin = 4
    bounce_time = 400
    ret_func = None

    def __init__(self, ret_func=None, pin=4, bounce_time=400, edge="falling"):
        Switch.__init__(self, ret_func=None)
        self.pin = pin
        self.bounce_time = 400
        self.ret_func = None

        global GPIO
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def close(self):
        pass

    def start_detection(self):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self._detected, bouncetime=self.bounce_time)

    def stop_detection(self):
        GPIO.remove_event_detect(self.pin)

