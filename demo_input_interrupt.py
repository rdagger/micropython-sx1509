"""SX1509 demo (Input Interrupt).
This example combines the SX1509's read_pin and interrupt
output functionalities. When a button connected to pin 2 is
pressed, the SX1509 will generate an active-low interrupt,
signalling to the Pico that a button has been pressed.

Hardware Hookup:
SX1509 Breakout ---- Pico --------- Breadboard
    GND ------------ GND
    3V3 ------------ 3V3(Out)
    SDA ------------ SDA (GPIO2)
    SCL ------------ SCL (GPIO3)
    2 ------------------------------]BTN[----GND
    INT ------------ GPIO16

Derived from SparkFun_SX1509_Arduino_Library
Original source: https://github.com/sparkfun/SparkFun_SX1509_Arduino_Library
"""
from time import sleep
from machine import I2C, Pin  # type: ignore
from sx1509 import Expander, PinModes, FALLING

i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))  # Pico I2C bus 1
expander = Expander(i2c)

SX1509_BUTTON_PIN = 2  # Active-low button


def button_pressed(pin):
    print(f"Raspberry Pi Pico interrupt triggered {pin}.")
    int_status = expander.interrupt_source()
    print(f"SX1509 Interrupt Status = 0b{int_status:b}")
    # Determine which buttons were pressed
    pressed = [bit for bit in range(16) if int_status & (1 << bit)]
    print(f"Button(s) pressed: {pressed}.")


PICO_INT_PIN = 16  # SX1509 interrupt outputs to Pico GPIO 16
# Set up GPIO pin on Pico as input with a pull-up to read interrupt signal
int_pin = Pin(PICO_INT_PIN, Pin.IN, Pin.PULL_UP)
# Initialize interrupt handler on Pico pin to fire handler on falling
int_pin.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)


def test():
    """Test code."""
    # Use a pull-up resistor on the button's input pin. When
    # the button is pressed, the pin will be read as LOW:
    expander.pin_mode(SX1509_BUTTON_PIN, PinModes.INPUT_PULLUP)

    # Enable interrupt on button pin for falling edge (button press)
    expander.enable_interrupt(SX1509_BUTTON_PIN, FALLING)

    # Set global debounce time to 32ms
    expander.debounce_time(32)

    # Enable debounce on the button pin
    expander.debounce_enable(SX1509_BUTTON_PIN)

    try:
        while True:
            sleep(1)  # Reduce CPU load
    except KeyboardInterrupt:
        print("\nCtrl-C pressed to exit.")
    finally:
        expander.reset()


test()
