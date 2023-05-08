from machine import PWM, Pin
from time import sleep_ms, mktime, gmtime
from device import IO, LED, Time, Files

# Filen er ufuldstændig og er sikkert fyldt med fejl (:

class Rotation:

    def __init__(self, esc_data1:int = 2, esc_data2:int = 3) -> None:
        self.esc_data_pin1 = esc_data1
        self.esc_data_pin2 = esc_data2

        self.io = IO()
        self.led = LED()
        self.time = Time()
        self.files = Files()

    def get_rotation_interval(self) -> int:
        rotation_interval = self.io.check_setting_turn_rate() # returnerer int der siger hvor ofte (i uger) den skal rotere
        print("rotation interval", rotation_interval)
        return rotation_interval
    
    def save_next_rotation(self, time) -> None:
        self.files.write_settings({"next_rotation":time})
    
    def pseudo_rotate(self):
        print("rotating for 5 seconds")
        self.led.led_rainbow_trail(seconds=5)
        print("rotation done")
    
    def rotate(self) -> None:
        self.pseudo_rotate()
    
    def is_time_to_rotate(self):    #startup.io.check_setting_turn_rate(), startup.files.read_settings()
        # Der skal være try/except på loopet
        current_unixtime = self.time.time_now()
        settings_dict = self.files.read_settings()
        print("current time is:", self.time.format_time(current_unixtime))

        # Læs settings for at finde next rotation
        try: # Der er gemt en next rotation
            next_rotation = settings_dict["next_rotation"]
        except KeyError as e: # Der er IKKE gemt en next rotation
            next_rotation = None

        if next_rotation == None or current_unixtime > next_rotation:
            print("Fetching new timezone-data") # <---------------------------------------------------------------------- #DEBUG

            print("Der er ingen setting, roter nu, gem næste tid")
            week = 60*60*24*7
            rotation_interval = self.get_rotation_interval()
            next_rotation = self.time.time_now()[1] + week * rotation_interval
            
            





            
            print(next_rotation)
            print(gmtime(next_rotation))



            self.wifi.connect() # Indtil metoden med login er lavet køres denne, her bruges default credentials som defineres i WiFi.__init__()
            
    
if __name__ == "__main__":
    test = Rotation()
    #test.time_to_rotate()

    print(test.files.read_settings())
