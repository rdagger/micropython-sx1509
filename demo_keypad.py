"""SX1509 demo (Keypad).

This example demonstrates how to use the SX1509's keypad engine to monitor a
matrix of button inputs.  For this example, we'll wire the SX1509 up to a
12-pad keypad.

Hardware Hookup:
SX1509 Breakout ---- Pico --------- Breadboard
    GND ------------ GND
    3V3 ------------ 3V3(Out)
    SDA ------------ SDA (GPIO2)
    SCL ------------ SCL (GPIO3)
      0 ------------ Keypad Row 1 (Pin 3)  # Keypad pinouts may vary
      1 ------------ Keypad Row 2 (Pin 8)
      2 ------------ Keypad Row 3 (Pin 7)
      3 ------------ Keypad Row 4 (Pin 5)
      8 ------------ Keypad Col 1 (Pin 4)
      9 ------------ Keypad Col 2 (Pin 2)
     10 ------------ Keypad Col 3 (Pin 6)

         C O L U M N S
    Pins | 4 | 2 | 6 |
      ----------------
    R 3  | 1 | 2 | 3 |
      ----------------
    O 8  | 4 | 5 | 6 |
      ----------------
    W 7  | 7 | 8 | 9 |
      ----------------
    S 5  | * | 0 | # |
      ----------------

Derived from SparkFun_SX1509_Arduino_Library
Original source: https://github.com/sparkfun/SparkFun_SX1509_Arduino_Library
"""
from time import sleep_ms
from machine import I2C, Pin  # type: ignore
from sx1509 import Expander, PinModes, HIGH, LOW

i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))  # Pico I2C bus 1
expander = Expander(i2c)

KEY_ROWS = 4
KEY_COLS = 3

KEY_MAP = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

# Specify the number of rows and columns.
# Note: we don't get to pick which pins the SX1509 connects
# to each row/column. They go up sequetially on
# pins 0-7 (rows), and 8-15 (columns)
KEY_ROWS = 4  # Number of rows in the keypad
KEY_COLS = 3  # Number of columns in the keypad

# Sleep time range: 128 ms - 8192 ms (powers of 2) 0=OFF
# After a set number of milliseconds, the keypad engine
# will go into a low-current sleep mode.
SLEEP_TIME = 256

# Scan time range: 1-128 ms, powers of 2
# Scan time defines the number of milliseconds devoted to
# each row in the matrix.
SCAN_TIME = 2

# Debounce time range: 0.5 - 64 ms (powers of 2)
# Debounce sets the minimum amount of time that must pass
# before a button can be pressed again.
# Note: Scan time must be greater than debounce time
DEBOUNCE_TIME = 1

# Set up the keypad engine
expander.keypad(KEY_ROWS, KEY_COLS, SLEEP_TIME, SCAN_TIME, DEBOUNCE_TIME)


def test():
    """Test code."""
    try:
        while True:
            key_data = expander.read_keypad()
            if key_data != 0:
                # A key was pressed
                # Format the key_data into readable binary
                key_parts = [(key_data >> (4 * i)) & 0xF
                             for i in range(4)][::-1]
                formatted_key_data = " ".join(f"{part:04b}"
                                              for part in key_parts)
                print(f"Key data: {formatted_key_data}")
                # Find the active row and columns
                row = expander.get_row(key_data)
                col = expander.get_col(key_data)
                # Get key pressed from key map
                key = KEY_MAP[row][col]
                print(f"Row: {row}, Column: {col}, Key: {key}")
            sleep_ms(100)
    except KeyboardInterrupt:
        print("\nCtrl-C pressed to exit.")
    finally:
        expander.reset()


test()
