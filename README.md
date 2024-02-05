A micropython clock implementation on esp32 with a ULN2003 (or eg 4 logic level MOSFETs should work). 
Setup is pretty straightforward:
1. Flash the micropython firmware onto your esp32by following the steps in the documentation here:
https://docs.micropython.org/en/latest/esp32/tutorial/intro.html

Alternatively Thonny IDE will do it for you and will also take care of transferring the python files onto the device:
https://thonny.org/

Open a serial connection to the board in your preferred manner (Thonny works well). 
Connect to wifi (it's used to keep time).
Upload these files to the board and reset.

You can then access the board over wifi via the WebREPL (connect with Thonny or using the web client: https://github.com/micropython/webrepl)
There is only really 1 function you may need:

my_clock.calibrate_hands(hour, minute) <- Just insert the current position of the hour (0-11) and minute (0-59) hands.
The position of the hands is persisted in nonvolatile storage (or a file if not available) and will move back to the correct time even after being unpowered.

PWM based "microstepping" is implemented to keep the motor as quiet as possible.

At the next minute, the clock will move the hands to the correct position and time.
If your motor has a differnet number of steps (apparently some do) you can change the number of steps the motor is initiated with in boot.py


