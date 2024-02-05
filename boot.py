# boot.py -- run on boot-up
import clock, machine, network, os, time, webrepl, webrepl_cfg
from store import get_store
from machine import Pin, PWM, soft_reset as sr

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(webrepl_cfg.WLAN_SSID, webrepl_cfg.WLAN_PASS)

CYCLES_PER_REVOLUTION = 32 / 4
MOTOR_GEAR_RATIO = 64
CLOCK_GEAR_RATIO = 90 / 12

PWM_FREQ = 156250
MICROSTEPS = 10

p = Pin(48, Pin.PULL_DOWN)
# Setup the stepper controller on the relevant pins
motor = clock.Stepper([
        PWM(Pin(18), freq=PWM_FREQ),
        PWM(Pin(8), freq=PWM_FREQ),
        PWM(Pin(3), freq=PWM_FREQ),
        PWM(Pin(46), freq=PWM_FREQ),
    ],
    cycles_per_rotation=CYCLES_PER_REVOLUTION * MOTOR_GEAR_RATIO * CLOCK_GEAR_RATIO,
    microsteps=MICROSTEPS,
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