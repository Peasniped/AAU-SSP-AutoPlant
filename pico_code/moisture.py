from machine import ADC, Pin
from time import sleep_ms
import _thread

# <------------------------------------------------------------------------------ #TODO
# Der er fejl i filen som skal rettes.
# Den skal fx bruge LED-klassen fra Device.py

class Moisture:

    def __init__(self, power_pin:int = 27, data_pin:int = 26) -> None:    
        self.MAX_VALUE = 65535 # ADC er 16 bits, så maxværdi er 65535
        self.MIN_VALUE = 17900 # 17900 er en potte der er godt fyldt
        self.MIN_VALUE_ADJUSTED = self.MAX_VALUE - self.MIN_VALUE

        self.sensor_power = Pin(power_pin, Pin.OUT)
        self.sensor_data = ADC(Pin(data_pin))
        pass

    def read_moisture(self) -> int:
        self.sensor_power.on()
        sleep_ms(25)
        value = int(self.sensor_data.read_u16())
        self.sensor_power.off()
        print(f"Moisture Value: {value}") #DEBUG
        return value
    
    def moisture_percent(self) -> int:
        reading = self.read_moisture()
        reading -= self.MIN_VALUE
        reading = - reading + self.MIN_VALUE_ADJUSTED
        percent = int(round((reading / self.MIN_VALUE_ADJUSTED) * 100))
        print(f"Moisture Percent: {percent}%") #DEBUG
        return percent
    
class Device:

    def __init__(self, led_brightness:int = 25) -> None:
        self.TOLERANCE_DRY = 30
        self.TOLERANCE_NORMAL = 50
        self.TOLERANCE_WET = 90 #70

        self.wetness_setting = 0
        self.setting_wet = Pin(14, Pin.IN, Pin.PULL_DOWN)
        self.setting_dry = Pin(15, Pin.IN, Pin.PULL_DOWN)
        self.moisture_sensor = Moisture()

    def read_settings(self) -> None:
        if self.setting_dry.value() == 1:
            print("the plant likes the dirt dry") #DEBUG
            self.wetness_setting = self.TOLERANCE_DRY
        elif self.setting_wet.value() == 1:
            print("the plant likes the dirt wet") #DEBUG
            self.wetness_setting = self.TOLERANCE_WET
        else:
            print("the plant likes the dirt normal") #DEBUG
            self.wetness_setting = self.TOLERANCE_NORMAL
    
    def decide_flash(self) -> None: # Skal flyttes til Moisture-klassen
        moist = self.moisture_sensor.moisture_percent()
        if moist <= self.wetness_setting:
            print("Plant is too dry!\n") #DEBUG
            self.led_flash(3)
        else:
            print("Plant is sufficiently wet!\n") #DEBUG
    
    def sleep_min(self, minutes:int = 1) -> None:
        minute = 1000 * 6001
        sleep_ms(minutes*minute)


if __name__ == "__main__": # Ved ikke lige hvad jeg har haft gang i herunder
    test = Device(led_brightness=25)

    test.led_flash()
    new_thread = _thread.start_new_thread(test.wait_for_clear, ())

    for i in range(11):
        print(i)
        sleep_ms(1000)
    test.done = True
    

    
    """
    while True:
        test.read_settings()
        test.decide_flash()
        test.sleep_min(3)
        #sleep_ms(5000)
    """
