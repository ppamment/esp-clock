# MicroPython Clock Project with 28BYJ-48 Stepper and ULN2003

This project involves implementing a clock using a 28BYJ-48 stepper motor driven by a ULN2003 or equivalent (e.g., 4 logic level MOSFETs). It's designed for enthusiasts looking for a straightforward setup with a casual tone.

## Setup Instructions

### Flashing the MicroPython Firmware

1. **Flash the MicroPython firmware onto your ESP32.** 
Follow the steps outlined in the official documentation: [MicroPython ESP32 Tutorial](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)

Alternatively, you can use the Thonny IDE, which streamlines the process by handling firmware flashing, file transfer, and connecting to the REPL via USB and Wi-Fi. For details, visit: [Thonny IDE](https://thonny.org/), specifically the `Run -> Configure Interpreter` section.

### Establishing Connections

2. **Establish a serial connection** using your preferred method.
3. **Connect your ESP32 to Wi-Fi** for time synchronization (as covered in the MicroPython documentation).
4. **Configure WebREPL for Wi-Fi access.** Execute the following in your REPL:
   `import webrepl_setup`
5. Add WLAN_SSID and WLAN_PASS to webrepl_cfg as ESP32 does not implement wifi credentials persistence.
 - If you don't want to do this, comment lines 6-11 in boot.py

### Uploading Files

5. **Clone or download this repository.**
6. **Upload all files to the filesystem root** of your ESP32.
7. **Perform a soft reset** with the following commands:
   `import machine`
   `machine.soft_reset()`

## Running the Clock

- After the reset, the clock should start running.
- Access the board over USB or Wi-Fi via WebREPL using Thonny or the [WebREPL web client](https://github.com/micropython/webrepl).
- **Calibrate the clock hands if needed:** Use `my_clock.calibrate_hands(hour, minute)` replacing 'hour' (0-11) and 'minute' (0-59) with the current positions.
- At the next minute, the clock will automatically adjust the hands to the correct time.
- The clock hands' positions are saved in nonvolatile storage (or a file, if NV storage is unavailable) each time they move, allowing the clock to remember their positions even after a power loss.

## Additional Configuration

- If your motor has a different step count, modify the step count in `boot.py`.
- PWM-based microstepping is implemented for quieter motor operation.
- If needed you can also adjust the PWM frequency and number of microsteps in `boot.py`.

**Note:** This project is intended for hobbyists and DIY enthusiasts. It assumes a basic understanding of MicroPython, ESP32, and stepper motor operation.