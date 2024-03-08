"""SX1509 demo (Breathe).
This example demonstrates the SX1509's set-it-and-forget-it
breathe function. The SX1509 will pulse an LED, smoothly
ramping its brightness up-then-down. We'll set the pin up as
an ANALOG_OUTPUT, and call io.breathe() all in setup(), then
watch the LED pulse by itself in loop().

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

    # Breathe an LED: 500ms LOW, 600ms HIGH,
    # 500ms to rise from low to high
    # 250ms to fall from high to low
    # The timing parameters are in milliseconds, but they
    # aren't near 100% exact. The library will estimate to try to
    # get them as close as possible. Play with the clock
    # divider to maybe get more accurate timing.
    expander.breathe(SX1509_LED_PIN, 500, 600, 500, 250)


# Main loop does nothing: SX1509 handles the breathing
    try:
        while True:
            sleep(1)  # Reduce CPU load
    except KeyboardInterrupt:
        print("\nCtrl-C pressed to exit.")
    finally:
        expander.reset()


test()
