from machine import ADC, Pin
from time import sleep_ms
from device import IO, LED

class Moisture:

    def __init__(self, power_pin:int = 27, data_pin:int = 26, debug_terminal:bool = False) -> None:    
        self.MAX_VALUE = 65535 # ADC er 16 bits, så maxværdi er 65535
        self.MIN_VALUE = 17900 # 17900 er en potte der er lettere overvandet
        self.MIN_VALUE_ADJUSTED = self.MAX_VALUE - self.MIN_VALUE
        
        self.debug_terminal = debug_terminal

        self.too_dry_threshold_dry = 40 
        self.too_dry_threshold_normal = 55
        self.too_dry_threshold_wet = 70

        self.sensor_power = Pin(power_pin, Pin.OUT)
        self.sensor_data = ADC(Pin(data_pin))

        self.io = IO()
        self.led = LED(led_brightness=100)

    def read_moisture(self) -> int:
        self.sensor_power.on()
        sleep_ms(25)
        value = int(self.sensor_data.read_u16())
        self.sensor_power.off()
        if self.debug_terminal: print(f"Moisture Value: {value}") # <-------------------------------- #DEBUG
        return value
    
    def moisture_percent(self) -> int:
        reading = self.read_moisture()
        reading -= self.MIN_VALUE
        reading = - reading + self.MIN_VALUE_ADJUSTED
        percent = int(round((reading / self.MIN_VALUE_ADJUSTED) * 100))
        if self.debug_terminal: print(f"Moisture Percent: {percent}%") # <---------------------------- DEBUG
        return percent
    
    def get_threshold(self) -> int:
        dryness_setting = self.io.check_setting_wetness()
        if dryness_setting == "dry":
            threshold = self.too_dry_threshold_dry
        elif dryness_setting == "normal":
            threshold = self.too_dry_threshold_normal
        else:
            threshold = self.too_dry_threshold_wet
        return threshold
    
    def too_dry(self) -> bool:
        if self.moisture_percent() < self.get_threshold():
            return True
        else: return False

    def flash(self) -> None:
        self.led.led_flash_double()
