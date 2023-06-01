from machine import Pin
from time import mktime, localtime, gmtime, sleep
from device import Microcontroller, LED_Strip, Time

class Motor:
    def __init__(self, pwm_duty_cycle:int, esc_data1:int = 2, esc_data2:int = 3, debug_terminal:bool = False) -> None:
        self.debug_terminal = debug_terminal

        self.io = Microcontroller()
        self.led = LED_Strip()
        self.time = Time()

        self.next_rotation = 0
        self.position = 0

    def get_rotation_interval(self) -> int:
        rotation_interval = self.io.check_setting_turn_rate() # returnerer int der siger hvor ofte (i uger) den skal rotere
        if self.debug_terminal: print("rotation interval", rotation_interval) # <----------------------------------------------------------- #DEBUG
        return rotation_interval

    def is_time_to_rotate(self) -> bool:
        time = self.time.get_uptime()
        
        if self.next_rotation == 0 or time > self.next_rotation:
            if self.debug_terminal: print("Der er ingen setting, roter nu, gem næste tid") # <---------------------------------------------- #DEBUG
            # week = 60*60*24*7 # Antal sekunder på en uge
            week = 10 # <------------------------------------------------------------------------------------------------------------------- #DEBUG
            rotation_interval = self.get_rotation_interval()
            self.next_rotation = time + week * rotation_interval
            if self.debug_terminal: print(f"It's time to rotate -> Current time: {time} next rotation time is: {self.next_rotation}") # <--- #DEBUG
            return True
        else:
            if self.debug_terminal: print(f"Not time to rotate -> Current time: {time} next rotation time is: {self.next_rotation}") # <---- #DEBUG
            return False  


class Step_Motor(Motor):
    def __init__(self, esc_data1: int = 2, esc_data2: int = 3, rotation_time:int = 5, debug_terminal:bool = False) -> None:
        super().__init__(esc_data1, esc_data2, debug_terminal)
        self.debug_terminal = debug_terminal
        self.rotation_time = rotation_time

        self.stepper_in1 = Pin(21, Pin.OUT)
        self.stepper_in2 = Pin(20, Pin.OUT)
        self.stepper_in3 = Pin(19, Pin.OUT)
        self.stepper_in4 = Pin(18, Pin.OUT)

        self.position = self.read_position()

    def rotate(self) -> None:
        if self.position < 6:
            self.stepper_rotate(250, 0.5)
            self.position += 1
            self.save_position(self.position)
        else: 
            self.rotate_return()
            self.position = 0
            self.save_position(self.position)

    def rotate_return(self) -> None:
        steps = 250 * 6
        self.stepper_rotate(steps, 3, direction = -1)

    def save_position(self, position) -> None:
        if position > 6:
            position = 0
        self.position = position
    
    def read_position(self) -> int:
        return self.position

    def stepper_rotate(self, steps:int, time:float, direction:int = 1) -> None:
        delay = time / steps
        if direction == 1:
            SEQUENCE = [[1, 0, 0, 1],
                        [1, 0, 0, 0],
                        [1, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 1, 0],
                        [0, 0, 1, 0],
                        [0, 0, 1, 1],
                        [0, 0, 0, 1]]
        else: 
            SEQUENCE = [[0, 0, 0, 1],
                        [0, 0, 1, 1],
                        [0, 0, 1, 0],
                        [0, 1, 1, 0],
                        [0, 1, 0, 0],
                        [1, 1, 0, 0],
                        [1, 0, 0, 0],
                        [1, 0, 0, 1]]
            
        if self.debug_terminal: print("Motor turning\n") # <-------------------------------------------------------------------------------- #DEBUG
        
        for _ in range(steps):
            for step in range(8):
                self.stepper_in1.value(SEQUENCE[step][0])
                self.stepper_in2.value(SEQUENCE[step][1])
                self.stepper_in3.value(SEQUENCE[step][2])
                self.stepper_in4.value(SEQUENCE[step][3])
                sleep(delay)
        
        self.stepper_in1.value(0)
        self.stepper_in2.value(0)
        self.stepper_in3.value(0)
        self.stepper_in4.value(0)


if __name__ == "__main__":
    test = Step_Motor()
    interval = 3

    for i in range(13):
        test.rotate()
        print("position:", test.position)
        sleep(interval)