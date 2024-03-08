"""SX1509 demo (Keypad Interrupt).

This example demonstrates how to use the SX1509's keypad
engine to monitor a matrix of button inputs. The SX1509's
interrupt output is monitored to check for button presses.

Hardware Hookup:
SX1509 Breakout ---- Pico --------- Breadboard
    GND ------------ GND
    3V3 ------------ 3V3(Out)
    SDA ------------ SDA (GPIO2)
    SCL ------------ SCL (GPIO3)
    INT ------------ GPIO16
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
from sx1509 import Expander

i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))  # Pico I2C bus 1
expander = Expander(i2c)

PICO_INT_PIN = 16  # SX1509 interrupt outputs to Pico GPIO 16
# Set up GPIO pin on Pico as input with a pull-up to read interrupt signal
int_pin = Pin(PICO_INT_PIN, Pin.IN, Pin.PULL_UP)

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
    # Compared to the keypad in demo_keypad.py, this keypad example
    # is a bit more advanced. The following varaibles are used to check
    # if a key is being held down, or has been released to better
    # emulate the operation of a computer keyboard.
    previous_key_data = 0  # Stores last key pressed
    hold_count = release_count = 0  # Count durations
    hold_count_max = 100  # Key hold limit
    release_count_max = 100  # Release limit
    try:
        while True:
            if int_pin.value() == 0:  # Check if interrupt fired (low)
                key_data = expander.read_keypad()
                # Find the active row and columns
                row = expander.get_row(key_data)
                col = expander.get_col(key_data)
                # Get key pressed from key map
                key = KEY_MAP[row][col]
                if key_data != previous_key_data:
                    hold_count = 0  # Reset hold-down count
                    print(f"Key: {key}, Row: {row}, Column: {col}")
                else:  # If the button's being held down
                    hold_count += 1  # Increment holdCount
                    if hold_count > hold_count_max:  # If it exceeds threshold
                        print(f"Key: {key}, " +
                              f"Hold Count: {hold_count}, " +
                              f"Release Count: {release_count}")
                release_count = 0  # Clear the releaseCount variable
                previous_key_data = key_data  # Update previousKeyData

            # If no keys pressed continuously increment releaseCount.
            release_count += 1
            if release_count >= release_count_max:
                release_count = 0
                previous_key_data = 0
            sleep_ms(1)  # Gives release_count_max a more intuitive unit
    except KeyboardInterrupt:
        print("\nCtrl-C pressed to exit.")
    finally:
        expander.reset()


test()
