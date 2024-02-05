from machine import  Timer
from stepper import Stepper
import micropython
import ntptime
import time



class Clock:
    """
    Runs a clock by synchronising with ntptime over network every 60s.
    The current clock position is stored in the store provided
    """
    store = None    
    minutes: int
    microsteps: int
    
    def __init__(self, stepper: Stepper, store, timer_no: int = 0):
        self.stepper = stepper
        self.store = store
        self.minutes = self.read_position()
        self.timer = Timer(timer_no)
        
    def read_position(self) -> int:
        return self.store.get("time")
    
    def write_position(self, position: int):
        self.store.set("time", position)
        
    @staticmethod
    def get_real_minutes() -> int:
        real_time = time.localtime(ntptime.time())
        return (int(real_time[3]) % 12)*60 + real_time[4]
    
    def set_position(self, target_minutes: int, rpm: float = 1/5):
        difference = (target_minutes - self.minutes) % 720 # 720 minutes in 12 hrs
        minutes_to_move = difference - 720 if difference > 360 else difference
        print(f"Moving {minutes_to_move}...")
        self.stepper.step(minutes_to_move/60, rpm)
        self.minutes = target_minutes
        self.write_position(target_minutes)
    
    def update_time(self, _ = None):
        real_minutes = self.get_real_minutes()
        print(f"Real minutes: {real_minutes}\n Clock minutes: {self.minutes}\n")

        while self.minutes != real_minutes:
            self.set_position(real_minutes, 2 if abs(self.minutes - real_minutes) > 2 else 1/5)
            real_minutes = self.get_real_minutes()

    def tick_callback(self, timer):
        micropython.schedule(self.update_time, 0)

    def calibrate_hands(self, hour, minute):
        self.minutes = hour*60 + minute
        self.write_position(self.minutes)
                
    def start(self, update_ms = 60000):
        self.update_time()
        self.timer.init(period=update_ms, mode=Timer.PERIODIC, callback=self.tick_callback)
    
    def stop(self):
        self.timer.deinit()
            
            
        
 












