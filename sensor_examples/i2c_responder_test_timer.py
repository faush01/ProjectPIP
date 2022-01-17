import micropython
from machine import Pin, I2C, Timer
import time
import _thread

# Local
from i2c_responder import I2CResponder

##########################################################################
# Helper Functions

def format_hex(_object):
    """Format a value or list of values as 2 digit hex."""
    try:
        values_hex = [to_hex(value) for value in _object]
        return '[{}]'.format(', '.join(values_hex))
    except TypeError:
        # The object is a single value
        return to_hex(_object)
    
def to_hex(value):
    return '0x{:02X}'.format(value)

##########################################################################
# Set up the I2C responder

I2C_FREQUENCY = 100000

RESPONDER_I2C_DEVICE_ID = 0
RESPONDER_ADDRESS = 0x41
GPIO_RESPONDER_SDA = 0
GPIO_RESPONDER_SCL = 1

i2c_responder = I2CResponder(
    RESPONDER_I2C_DEVICE_ID, sda_gpio=GPIO_RESPONDER_SDA, scl_gpio=GPIO_RESPONDER_SCL, responder_address=RESPONDER_ADDRESS
)

print('I2CResponder v' + i2c_responder.VERSION)

##########################################################################
# Sensor data

sensor_data = bytearray(10)
#[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

##########################################################################
# Sensor IO Block

counter = 0
sensor_timer = Timer()
sensor_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)

def scheduled_handler(pin):
    global counter
    if sensor_pin.value():
        print("Signal Trip : " + str(counter))
        counter += 1
        if counter > 255:
            counter = 0
        sensor_data[0] = counter
        
def signal_handler(pin):
    micropython.schedule(scheduled_handler, pin)
        
def debounce(pin):
    sensor_pin.irq(handler=None)
    time.sleep_ms(1)
    #print("Interrupt Detected")
    sensor_timer.init(mode=Timer.ONE_SHOT, period=50, callback=signal_handler)
    sensor_pin.irq(handler=debounce)
    
sensor_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=debounce)

##########################################################################
# Control Reader Block
# used for testing, this uses the second I2C interface to read the data
# uses a period timer and thread as the responder is blocking
# you need to connect the I2C pins and use pull up resistors for this to work

CONTROLLER_I2C_DEVICE_ID = 1
GPIO_CONTROLLER_SDA = 2
GPIO_CONTROLLER_SCL = 3

i2c_controller = I2C(
    CONTROLLER_I2C_DEVICE_ID,
    scl=Pin(GPIO_CONTROLLER_SCL),
    sda=Pin(GPIO_CONTROLLER_SDA),
    freq=I2C_FREQUENCY,
)

print('Scanning I2C Bus for Responders...')
responder_addresses = i2c_controller.scan()
print('I2C Addresses of Responders found: ' + format_hex(responder_addresses))
print()

thread_lock = _thread.allocate_lock()
data = bytearray(10)
count = 0

def timer_thread_call(controller, thread_lock): 
    global data
    global count
    with thread_lock:
        controller.readfrom_into(RESPONDER_ADDRESS, data)
    print("Controller : Received data : (" + str(count) + ") " + format_hex(data))
    count += 1
    
def timer_function(timer_obj):
    _thread.start_new_thread(timer_thread_call, (i2c_controller, thread_lock,))

timer = Timer()
timer.init(period=1000, mode=Timer.PERIODIC, callback=timer_function)

##########################################################################
# Responce Block

def scheduled_send_data(value):
    #print('Responder  : Transmitted : ' + format_hex(sensor_data))
    for i in sensor_data:
        #print('Responder  : Transmitted : ' + format_hex(i))
        i2c_responder.put_read_data(i)  

while True:    
    while not i2c_responder.read_is_pending():
        pass
    micropython.schedule(scheduled_send_data, None)       
