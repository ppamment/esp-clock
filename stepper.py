from machine import PWM
import asyncio, time

MAX_DUTY = (2**16 - 1) * 3 // 4

HALF_STEP_DRIVE = [
    [0, 0, 1, 1],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [0, 0, 0, 1],
]

FULL_STEP_DRIVE = [
   [0, 0, 0, 1],
   [0, 0, 1, 0],
   [0, 1, 0, 0],
   [1, 0, 0, 0]
]

class Stepper():
    """
    Controls a stepper motor.
    Uses a PWM based microstepping approach that works even with stepper drivers that do not support microstepping.
    Simple transistors are sufficient to achieve good results.
    """
    def __init__(self, pins: list(PWM), cycles_per_rotation, mode = HALF_STEP_DRIVE, microsteps = 8):
        self.mode = mode
        self.pins = pins
        self.cycles_per_rotation = cycles_per_rotation
        self.microsteps = microsteps
        
    def step(self, rotations, rotations_per_minute):
        """Rotate specified number of full turns. +ve clockwise, -ve counter-clockwise"""
        try:
          if rotations < 0:
              direction = -1
              rotations = -rotations
          else:
              direction = 1
          
          if rotations >= float("inf"):
            steps = rotations
            us = rotations
            us_per_step = 1e6 / (self.cycles_per_rotation * rotations_per_minute / 60) 
          else:
              steps = int(rotations * self.cycles_per_rotation)
              us = (rotations / (rotations_per_minute / 60)) * 1e6
              us_per_step = us / steps
              
          print(f"Steps: {steps * direction}")
          print(f"Expected Duration: {us / 1e6}s")
          print(f"Calculated time per step: {us_per_step}us")
          
          counter = 0
          
          start = lap = time.ticks_us()
          while counter < steps:
              sleep_time = round(time.ticks_diff(time.ticks_add(start, round(us_per_step * (counter+1))), lap) / (len(self.mode) * self.microsteps))
              prev_bit = [0] * len(self.pins)
              for bit in self.mode[::direction]:
                  for i in range(self.microsteps):
                      # move frin current duty to the next in small steps 1/10th at a time
                      for j, pin in enumerate(self.pins):
                          pin.duty_u16(((self.microsteps-1-i)*pin.duty_u16() + (i+1)*bit[j]*MAX_DUTY) // self.microsteps)
                      time.sleep_us(sleep_time)
                  prev_bit = bit
              counter = counter + 1
              lap = time.ticks_us()
          
          end = time.ticks_us()
          print(f"Actual Duration: {(end-start) / 1e6}s")
          self.stop()
        except Exception as e:
          print(f"{e}")
        
    def stop(self):
        # Reset to 0, no holding, these are geared, you can't move them
        for i, pin in enumerate(self.pins):
            pin.duty_u16(0)