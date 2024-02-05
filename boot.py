# boot.py -- run on boot-up
import clock, machine, os, time, webrepl
from store import get_store
from machine import Pin, PWM, soft_reset as sr

p = Pin(48, Pin.PULL_DOWN)
# Setup the stepper controller on the relevant pins
motor = clock.Stepper([
        PWM(Pin(18), freq=156250),
        PWM(Pin(8), freq=156250),
        PWM(Pin(3), freq=156250),
        PWM(Pin(46), freq=156250),
    ],
    512 * 90 / 12 # Stepper has 512 steps, and the clock interface has a 90:12 gearing
)
# Keeps track of the current clock position in nonvolatile storage (or a file)
store = get_store()

my_clock = clock.Clock(motor, store)

try:
    # Run the clock
    time.sleep(2)
    my_clock.start()
except KeyboardInterrupt as e:
    my_clock.stop()
    
webrepl.start()