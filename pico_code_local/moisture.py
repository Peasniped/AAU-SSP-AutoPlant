from machine import ADC, Pin
from time import sleep_ms
from device import Microcontroller, LED_Strip

class Sensor:
    def __init__(self, power_pin:int = 27, data_pin:int = 26, debug_terminal:bool = False) -> None:
        """
        Initialize the Sensor class.

        This class represents a generic sensor and provides the basic functionality for interacting with sensors.

        Args:
            power_pin (int, optional): The pin number for the power pin of the sensor. Default is 27.
            data_pin (int, optional): The pin number for the data pin of the sensor. Default is 26.
            debug_terminal (bool, optional): Enable debug terminal output. Default is False.

        Returns:
            None
        """
        self.ADC_MAX_VALUE = 65535 # ADC er 16 bits, så maxværdi er 65535
        
        self.io = Microcontroller()
        self.led = LED_Strip()
        self.sensor_data = ADC(Pin(data_pin))
        

class Moisture(Sensor):

    def __init__(self, power_pin: int = 27, data_pin: int = 26, debug_terminal: bool = False) -> None:
        """
        Initialize the Moisture class.

        This class represents a moisture sensor and provides additional functionality for reading moisture levels.

        Args:
            power_pin (int, optional): The pin number for the power pin of the sensor. Default is 27.
            data_pin (int, optional): The pin number for the data pin of the sensor. Default is 26.
            debug_terminal (bool, optional): Enable debug terminal output. Default is False.

        Returns:
            None
        """
        super().__init__(power_pin, data_pin, debug_terminal)
        
        self.MIN_VALUE = 17900 # 17900 er en potte der er lettere overvandet
        self.MIN_VALUE_ADJUSTED = self.ADC_MAX_VALUE - self.MIN_VALUE
        
        self.debug_terminal = debug_terminal

        self.too_dry_threshold_dry = 30 
        self.too_dry_threshold_normal = 40
        self.too_dry_threshold_wet = 99


    def read_moisture(self) -> int:
        """
        Read the moisture level.

        This function reads the moisture level from the moisture sensor.

        Args:
            None

        Returns:
            int: The moisture level reading.
        """
        sleep_ms(25)
        value = int(self.sensor_data.read_u16())
        if self.debug_terminal: print(f"Moisture Value: {value}") # <----------------------------------- #DEBUG
        return value
    
    def moisture_percent(self) -> int:
        """
        Calculate the moisture level percentage.

        This function calculates the moisture level percentage based on the moisture sensor reading.

        Args:
            None

        Returns:
            int: The moisture level percentage.
        """
        reading = self.read_moisture()
        reading -= self.MIN_VALUE
        reading = - reading + self.MIN_VALUE_ADJUSTED
        percent = int(round((reading / self.MIN_VALUE_ADJUSTED) * 100))
        if self.debug_terminal: print(f"Moisture Percent: {percent}%") # <---------------------------- #DEBUG
        return percent
    
    def get_threshold(self) -> int:
        """
        Get the moisture threshold based on the dryness setting.

        This function retrieves the moisture threshold based on the dryness setting.

        Args:
            None

        Returns:
            int: The moisture threshold.
        """
        dryness_setting = self.io.check_setting_wetness()
        if dryness_setting == "dry":
            threshold = self.too_dry_threshold_dry
        elif dryness_setting == "normal":
            threshold = self.too_dry_threshold_normal
        else:
            threshold = self.too_dry_threshold_wet
        if self.debug_terminal: print(f"Moisture Setting: {dryness_setting}") # <--------------------- #DEBUG
        return threshold
    
    def too_dry(self) -> bool:
        """
        Check if the moisture level is too dry.

        This function compares the moisture level with the threshold and determines if it is too dry.

        Args:
            None

        Returns:
            bool: True if the moisture level is too dry, False otherwise.
        """
        moisture = self.moisture_percent()
        threshold = self.get_threshold()
        if self.debug_terminal: print(f"Moisture: {moisture}%, Threshold: {threshold}%\n") # <--------------------- #DEBUG
        if moisture < threshold:
            return True
        else: return False

    def flash(self) -> None:
        """
        Flash the LED strip.

        This function turns off the LED strip, waits for a short duration, and then flashes the LED strip twice.

        Args:
            None

        Returns:
            None
        """
        self.led.led_off()
        sleep_ms(20)
        self.led.led_flash_double()

if __name__ == "__main__":
    test = Moisture(debug_terminal=True)
    while True:
        if test.too_dry():
            test.flash()
        sleep_ms(1000)