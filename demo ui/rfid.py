# card tap for user login (step1)
import sys
from mfrc522 import SimpleMFRC522
from time import sleep
import Jetson.GPIO as GPIO

reader = SimpleMFRC522()
GPIO.setwarnings(False)

def card_tap():
    try:
        while True:
            id, text = reader.read()
            return id
            sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()
        raise


