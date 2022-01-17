from machine import Pin, I2C, Timer
import time
import _thread

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

I2C_FREQUENCY = 100000
RESPONDER_ADDRESS = 0x41

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

while True:
    i2c_controller.readfrom_into(RESPONDER_ADDRESS, data)
    print("Controller : Received data : (" + str(count) + ") " + format_hex(data))
    count += 1
    time.sleep(1)

