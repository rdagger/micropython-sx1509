"""SX1509 demo (Input).
This example demonstrates the SX1509's read_pin
functionality. A pin can either be set as an INPUT or
INPUT_PULLUP. We'll attach an active-low button to an 
INPUT_PULLUP input, then whenever the button read's LOW, we'll
read the state of another INPUT pin.

Hardware Hookup:
SX1509 Breakout ---- Pico --------- Breadboard
    GND ------------ GND
    3V3 ------------ 3V3(Out)
    SDA ------------ SDA (GPIO2)
    SCL ------------ SCL (GPIO3)
    0 ------------------------------]BTN[----GND
	8 ------------------------------Jumper (GND or 3.3V)

Derived from SparkFun_SX1509_Arduino_Library
Original source: https://github.com/sparkfun/SparkFun_SX1509_Arduino_Library
"""
from time import sleep
from machine import I2C, Pin  # type: ignore
from sx1509 import Expander, PinModes, LOW

i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))  # Pico I2C bus 1
expander = Expander(i2c)

SX1509_BUTTON_PIN = 0  # Active-low button
SX1509_INPUT_PIN = 8  # Floating or jumpered input

def test():
    """Test code."""
    # use pin mode to set input pins as either
    # INPUT or INPUT_PULLUP. Set up a floating (or jumpered to
    # either GND or 3.3V) pin to an INPUT:
    expander.pin_mode(SX1509_INPUT_PIN, PinModes.INPUT)

    # Use a pull-up resistor on the button's input pin. When
    # the button is pressed, the pin will be read as LOW:
    expander.pin_mode(SX1509_BUTTON_PIN, PinModes.INPUT_PULLUP)

    count = 0
    try:
        while True:
            # Use read_pin(<pin>) to check if an SX1509 input
            # pin is either HIGH or LOW.
            if expander.read_pin(SX1509_BUTTON_PIN) == LOW:
                # If the button is pressed (the pin reads LOW)
                # Print the status of the other pin:
                count += 1
                print(f"SX1509_INPUT_PIN status (count={count}):")
                # Read the pin to print either 0 or 1
                print(expander.read_pin(SX1509_INPUT_PIN))
            sleep(.1)  # Reduce CPU load
    except KeyboardInterrupt:
        print("\nCtrl-C pressed to exit.")
    finally:
        expander.reset()


test()
