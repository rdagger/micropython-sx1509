"""SX1509 demo (Output).

This simple example demonstrates the SX1509's digital output 
functionality. Attach an LED to SX1509 IO 15, or just look at
it with a multimeter. We're gonna blink it

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
from sx1509 import Expander, PinModes, HIGH, LOW

i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))  # Pico I2C bus 1
expander = Expander(i2c)

SX1509_LED_PIN = 15  # LED connected to SX1509's pin 15


def test():
    """Test code."""

    """Controls an LED's brightness via PWM."""
    # Set LED pin to ANALOG_OUTPUT (PWM)
    expander.pin_mode(SX1509_LED_PIN, PinModes.OUTPUT)

    try:
        while True:
            # Call write_pin(<pin>, <HIGH | LOW>) to set a SX1509
            # output pin as either 3.3V or 0V.
            expander.write_pin(SX1509_LED_PIN, HIGH)
            sleep_ms(500)
            expander.write_pin(SX1509_LED_PIN, LOW)
            sleep_ms(500)
    except KeyboardInterrupt:
        print("\nCtrl-C pressed to exit.")
    finally:
        expander.reset()


test()
