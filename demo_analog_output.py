"""SX1509 demo (Analog Output).

This example demonstrates the SX1509's pwm function.
Connect an LED to the SX1509's pin 15 (or any other pin, they
can all PWM!). The SX1509 can either sink or source current,
just don't forget your limiting resistor!

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
from time import sleep_ms
from machine import I2C, Pin  # type: ignore
from sx1509 import Expander, PinModes

i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))  # Pico I2C bus 1
expander = Expander(i2c)

SX1509_LED_PIN = 15  # LED connected to SX1509's pin 15


def test():
    """Test code."""

    """Controls an LED's brightness via PWM."""
    # Set LED pin to ANALOG_OUTPUT (PWM)
    expander.pin_mode(SX1509_LED_PIN, PinModes.ANALOG_OUTPUT)

    # Ramp brightness up from 0-255
    for brightness in range(256):
        expander.pwm(SX1509_LED_PIN, brightness)
        sleep_ms(2)  # Delay 2 milliseconds

    sleep_ms(500)  # Delay half-a-second

    # Ramp brightness down from 255-0
    for brightness in range(255, -1, -1):
        expander.pwm(SX1509_LED_PIN, brightness)
        sleep_ms(2)  # Delay 2 milliseconds

    sleep_ms(500)  # Delay half-a-second

    expander.reset()


test()
