import machine
import micropython
from machine import Timer
import time

# implement a high pressision pulse counter using interupts and timer ticks

counter = 0
timer = Timer()
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
last_signal = time.ticks_us()

def scheduled_handler(pin):
    global counter
    if button.value():
        global last_signal
        this_signal = time.ticks_us()
        time_since_last = time.ticks_diff(this_signal, last_signal)
        last_signal = this_signal
        print("Signal Trip : " + str(counter) + " : " + str(this_signal) + " : " + str(time_since_last))
        counter += 1    

def signal_handler(pin):
    micropython.schedule(scheduled_handler, pin)
    
def debounce(pin):
    button.irq(handler=None)
    time.sleep_ms(1)
    #print("Interrupt Detected")
    timer.init(mode=Timer.ONE_SHOT, period=50, callback=signal_handler)
    button.irq(handler=debounce)
    
button.irq(trigger=machine.Pin.IRQ_RISING, handler=debounce)

while True:
    
    time.sleep(1)
