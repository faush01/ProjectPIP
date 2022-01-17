from machine import Pin
from time import sleep

# simple example to test connection to pico

led = Pin(25, Pin.OUT)
reset = Pin(15, Pin.IN, Pin.PULL_DOWN)

while True:
    led.toggle()
    if reset.value():
        print("reset detected")
        break
    sleep(0.1)
    