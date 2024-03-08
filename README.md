# micropython-sx1509

This library provides a MicroPython port of the SparkFun SX1509 Arduino library, allowing you to control the SX1509 16-channel I/O expander with a Raspberry Pi Pico or any other MicroPython-compatible board. The SX1509 can handle multiple GPIO functionalities such as digital input/output, PWM, LED driver, and keypad reading, making it an excellent extension for projects requiring additional IOs.

## Installation

To use this library, you must first copy the `sx1509.py` file to your MicroPython device. This can be done using any MicroPython file transfer tool compatible with your system.

## Hardware Setup

To connect the SX1509 to your Raspberry Pi Pico, follow this basic wiring guide:

- **GND** on SX1509 to **GND** on Pico
- **3V3 (Out)** on SX1509 to **3V3 (Out)** on Pico
- **SDA** on SX1509 to **SDA (GPIO2)** on Pico
- **SCL** on SX1509 to **SCL (GPIO3)** on Pico

For specific functionalities like controlling an LED, connecting a button, or setting up a keypad, refer to the individual examples' hardware hookup sections.

## Examples Overview

This library includes several demos showcasing different features of the SX1509:

- **Analog Output (PWM):** Control the brightness of an LED connected to an SX1509 pin using PWM.
- **Blink:** Make an LED blink using the SX1509's built-in blink functionality.
- **Breathe:** Create a breathing LED effect with the SX1509's breathe function.
- **Input Interrupt:** Use the SX1509 to detect button presses and generate interrupts.
- **Input:** Read the state of a button connected to the SX1509.
- **Keypad Interrupt:** Monitor a keypad and detect button presses using the SX1509's interrupt feature.
- **Keypad:** Read button presses from a keypad using the SX1509.
- **Output:** Control an LED on and off using the SX1509's digital output feature.

Each example includes a detailed explanation of the hardware setup and the code required to run the demo.

## Acknowledgments

This library is a MicroPython port of the original [SparkFun SX1509 Arduino Library](https://github.com/sparkfun/SparkFun_SX1509_Arduino_Library). Special thanks to SparkFun for their work on developing and maintaining the Arduino version of this library.

## Contributing

Contributions to this library are welcome. Please submit pull requests or open issues on GitHub to suggest improvements or report bugs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

