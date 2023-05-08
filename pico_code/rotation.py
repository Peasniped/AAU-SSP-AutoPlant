from machine import PWM, Pin
from time import mktime, localtime, gmtime
from device import IO, LED, Time, Files

class Rotation:

    def __init__(self, esc_data1:int = 2, esc_data2:int = 3, debug_terminal:bool = False) -> None:
        self.esc_data_pin1 = esc_data1
        self.esc_data_pin2 = esc_data2

        self.debug_terminal = debug_terminal

        self.io = IO()
        self.led = LED()
        self.time = Time()
        self.files = Files()

    def get_rotation_interval(self) -> int:
        rotation_interval = self.io.check_setting_turn_rate() # returnerer int der siger hvor ofte (i uger) den skal rotere
        if self.debug_terminal: print("rotation interval", rotation_interval) # <----------------------------------------------------------- #DEBUG
        return rotation_interval
    
    def save_next_rotation(self, time) -> None:
        self.files.write_settings({"next_rotation":time})
    
    def pseudo_rotate(self):
        if self.debug_terminal: print("rotating for 5 seconds") # <------------------------------------------------------------------------- #DEBUG
        self.led.led_rainbow_trail(seconds=5)
        if self.debug_terminal: print("rotation done") # <---------------------------------------------------------------------------------- #DEBUG
    
    def rotate(self) -> None:
        self.pseudo_rotate()
    
    def is_time_to_rotate(self) -> bool:
        current_unixtime = mktime(localtime())
        settings_dict = self.files.read_settings()

        try: # Der er gemt en next_rotation
            next_rotation = int(settings_dict["next_rotation"])
        except KeyError as e: # Der er IKKE gemt en next_rotation
            next_rotation = None

        if next_rotation == None or current_unixtime > next_rotation:
            if self.debug_terminal: print("Der er ingen setting, roter nu, gem næste tid") # <---------------------------------------------- #DEBUG
            week = 60*60*24*7
            rotation_interval = self.get_rotation_interval()
            next_rotation = current_unixtime + week * rotation_interval
            self.files.write_settings({"next_rotation":next_rotation})
            if self.debug_terminal: print("next rotation time is:", self.time.format_time(gmtime(next_rotation))) # <----------------------- #DEBUG
            return True
        else:
            if self.debug_terminal: print("Not time to rotate: next rotation time is:", self.time.format_time(gmtime(next_rotation))) # <--- #DEBUG
            return False  
    

if __name__ == "__main__":
    test = Rotation()
    print("Is it time to rotate?:", test.is_time_to_rotate())
