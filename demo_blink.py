"""SX1509 demo (Blink).
This example demonstrates the SX1509's set-it-and-forget-it
blink function. We'll set the pin up as an OUTPUT, and call
io.blink() all in setup(), then watch the LED blink by itself
in loop().

Hardware Hookup:
SX1509 Breakout ---- Pico --------- Breadboard
    GND ------------ GND
    3V3 ------------ 3V3(Out)
    SDA ------------ SDA (GPIO2)
    SCL ------------ SCL (GPIO3)
    15 -----------------------------LED+
                                    LED- --////-- GND
                                           330Ω
Derived from SparkFun_SX1509_Arduino_Library
Original source: https://github.com/sparkfun/SparkFun_SX1509_Arduino_Library
"""
from time import sleep
from machine import I2C, Pin  # type: ignore
from sx1509 import Expander, PinModes

i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))  # Pico I2C bus 1
expander = Expander(i2c)

SX1509_LED_PIN = 15  # LED connected to SX1509's pin 15


def test():
    """Test code."""
    # Set LED pin to OUTPUT
    expander.pin_mode(SX1509_LED_PIN, PinModes.OUTPUT)

    # Start blinking: ~1000 ms LOW, ~500 ms HIGH
    expander.blink(SX1509_LED_PIN, 1000, 500)

# Main loop does nothing: SX1509 handles the blinking
    try:
        while True:
            sleep(1)  # Reduce CPU load
    except KeyboardInterrupt:
        print("\nCtrl-C pressed to exit.")
    finally:
        expander.reset()


test()
