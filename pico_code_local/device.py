from time import mktime, sleep_ms, localtime
from machine import Pin
from neopixel import NeoPixel
import _thread

class Microcontroller:
    def __init__(self) -> None:
        """
        Initialzes the Microcontroller object with relevant inputs.

        Args:
            self.input_reset : Button to restart product if.  
            self.input_2wk : Sets the product to rotate every 2 weeks.
            self.input_6wk : Sets the product to rotate every 6 weeks.
            self.input_dry : Sets soil preference to dry.        
            self.input_wet : Sets wet preference to wet.

        Returns:
            None.
        """
        self.input_reset = Pin(0, Pin.IN, Pin.PULL_DOWN)
        self.input_2wk = Pin(27, Pin.IN, Pin.PULL_DOWN)
        self.input_6wk = Pin(28, Pin.IN, Pin.PULL_DOWN)
        self.input_dry = Pin(22, Pin.IN, Pin.PULL_DOWN)
        self.input_wet = Pin(16, Pin.IN, Pin.PULL_DOWN)

    def check_reset(self) -> bool:
        """
        Checks if the product should be reset.

        Returns:
            True or False.
        """
        if self.input_reset.value() == 1:
            return True
        else: 
            return False
    
    def check_setting_wetness(self) -> str:
        """
        Checks the moisture setting determined by a physical switch set by user.

        Args:
            self.input_wet : Wet setting on switch.
            self.input_dry : Dry setting on switch.

        Returns:
            String
        """
        if self.input_wet.value() == 1:
            return "wet"
        elif self.input_wet.value() == 0 and self.input_dry.value() == 0:
            return "normal"
        elif self.input_dry.value() == 1:
            return "dry"
        else: 
            return "error"
        
    def check_setting_turn_rate(self) -> int:
        """
        Checks the rotation setting determined by a physical switch set by user.

        Args:
            input_2wk : 2 week rotation setting on switch.
            input_6wk : 6 week rotation setting on switch.

        Returns:
            Int
        """
        if self.input_2wk.value() == 1:
            return 2
        elif self.input_2wk.value() == 0 and self.input_6wk.value() == 0:
            return 4
        elif self.input_6wk.value() == 1:
            return 6  
        else: 
            return 0

class LED_Strip():
    def __init__(self, led_brightness:int = 25) -> None:
        """
        Initialize an LED strip object.

        Args:
            led_brightness (int): Brightness level of the LED strip. Value between 1 and 100,
                where 100 is the brightest and 1 is almost no light.

        Returns:
            None
        """
        self.LED_PIXELS = 47
        self.LED_BRIGHTNESS = led_brightness # Sættes ved instantiering af objektet - Værdi mellem 1 og 100, hvor 100 er mest lys og 1 er næsten ingen lys
        self.led_strip = NeoPixel(Pin(17), self.LED_PIXELS)
        self.trail_stop = False

        # Colors
        self.red = (255, 5, 0)
        self.green = (0,255, 5)
        self.blue = (0, 10, 255)

    def hue_to_rgb(self, angle:int) -> tuple:
            """
            Convert a hue angle to an RGB color.

            This function converts a hue angle (0-360) to an RGB color tuple.

            Args:
                angle (int): Hue angle value.

            Returns:
                tuple: RGB color tuple.
            """
            # Inspiration: Ontaelio(2016?) https://www.instructables.com/How-to-Make-Proper-Rainbow-and-Random-Colors-With-/
            if angle < 60:
                red = 255; green = round(angle*4.25-0.01); blue = 0
            elif angle < 120:
                red = round((120-angle)*4.25-0.01); green = 255; blue = 0
            elif angle < 180:
                red = 0; green = 255; blue = round((angle-120)*4.25-0.01)
            elif angle < 240:
                red = 0; green = round((240-angle)*4.25-0.01); blue = 255
            elif angle < 300:
                red = round((angle-240)*4.25-0.01); green = 0; blue = 255
            else:
                red = 255; green = 0; blue = round((360-angle)*4.25-0.01)
            return (red, green, blue)

    def led_on(self, color:tuple) -> None:
        """
        Turn on the LED strip with a specific color.

        This function sets all the LEDs on the strip to the specified color.

        Args:
            color (tuple): RGB color tuple.

        Returns:
            None
        """
        LED_R = int((color[0] / 100) * self.LED_BRIGHTNESS)
        LED_G = int((color[1] / 100) * self.LED_BRIGHTNESS)
        LED_B = int((color[2] / 100) * self.LED_BRIGHTNESS)

        for i in range(self.LED_PIXELS):
            self.led_strip[i] = (LED_R, LED_G, LED_B)
        self.led_strip.write()

    def led_on_single(self, pixel:int, color:tuple, write:bool = True) -> None:
        """
        Turn on a single LED with a specific color.

        This function sets a single LED on the strip to the specified color.

        Args:
            pixel (int): Index of the single LED pixel.
            color (tuple): RGB color tuple.
            write (bool): Whether to write the LED strip after setting the pixel color.

        Returns:
            None
        """
        LED_R = int((color[0] / 100) * self.LED_BRIGHTNESS)
        LED_G = int((color[1] / 100) * self.LED_BRIGHTNESS)
        LED_B = int((color[2] / 100) * self.LED_BRIGHTNESS)

        self.led_strip[pixel] = (LED_R, LED_G, LED_B)
        if write: self.led_strip.write()

    def led_off(self) -> None:
        """
        Turn off all the LEDs on the strip.

        This function sets all the LEDs on the strip to off (black).

        Args:
            None

        Returns:
            None
        """
        for i in range(self.LED_PIXELS):
            self.led_strip[i] = (0, 0, 0)
        self.led_strip.write()

    def led_flash_double(self, flashes:int = 1, on_time_ms:int = 60, delay_time_ms:int = 75, off_time_ms:int = 1500, color:tuple = (0,0,0)) -> None:
        """
        Flash the LED strip with a double flash pattern.

        This function flashes the LED strip with a double flash pattern,
        using the specified parameters.

        Args:
            flashes (int): Number of flash cycles.
            on_time_ms (int): Duration of each flash (in milliseconds).
            delay_time_ms (int): Delay between the two flashes (in milliseconds).
            off_time_ms (int): Delay between flash cycles (in milliseconds).
            color (tuple): RGB color tuple to use for the flashes.

        Returns:
            None
        """
        if color == (0,0,0):
            color = self.blue
        for i in range(flashes):
            self.led_on(color)
            sleep_ms(on_time_ms)
            self.led_off()
            sleep_ms(delay_time_ms)
            self.led_on(color)
            sleep_ms(on_time_ms)
            self.led_off()
            if not i + 1 == flashes:
                sleep_ms(off_time_ms)

    def led_rainbow_trail(self, interval:int = 20, trail_length:int = 25, seconds:int = 0, colors:tuple = ("rainbow","rainbow","rainbow")) -> None:
        """
        Create a rainbow trail effect on the LED strip.

        This function creates a rainbow trail effect on the LED strip,
        using the specified parameters.

        Args:
            interval (int): Time interval between each LED update (in milliseconds).
            trail_length (int): Number of LEDs in the trail.
            seconds (int): Duration of the effect (in seconds). Set to 0 for an infinite effect.
            colors (tuple): RGB color tuple(s) for the trail. Use "rainbow" for a rainbow trail.

        Returns:
            None
        """
        stopwatch = Stopwatch()
        self.trail_stop = False
        angle = 1
        led = 0
        direction = 1
        while self.trail_stop == False:
            if colors == ("rainbow","rainbow","rainbow"):
                color = self.hue_to_rgb(angle)
            else: color = colors
            self.led_on_single(led, color, False)
            if trail_length <= led:
                off_led = led - trail_length
                self.led_strip[off_led] = (0, 0, 0)
            else:
                off_led = self.LED_PIXELS - trail_length + led
                self.led_strip[off_led] = (0, 0, 0)
            self.led_strip.write()
            if led >= self.LED_PIXELS - 1: led = 0
            else: led += 1
            if angle == 255:
                direction = -1
            elif angle == 1:
                direction = 1
            angle += 1 * direction
            sleep_ms(interval)
            if stopwatch.get_time() >= seconds and seconds > 0: break
        self.trail_stop = True
        self.led_off()        

class Time:
    def rtc_fetch_unix_time(self) -> int:
        """Fetches the current time from the RTC and converts it to Unix time.
        
        Returns:
            int: The current time in Unix time format.
        """
        time = localtime() # RTC-tid -> Starttidspunkt er 1/jan 2021 00:00:00
        time = mktime(time) # Omdannes til Unixtime
        return time
    
    def get_uptime(self):
        """Calculates the system uptime in seconds since startup.
        
        Returns:
            int: The number of seconds since system startup.
        """ 
        time = self.rtc_fetch_unix_time()
        time -= 1609459200 # Omdan til sekunder siden opstart
        return time


class Stopwatch:
    def __init__(self) -> None:
        """
        Initializes a Stopwatch object.

        Args:
            None

        Returns:
            None
        """
        self.start_time = mktime(localtime())
        self.lap_times = []
    
    def get_time(self) -> int:
        """
        Calculates the elapsed time since the stopwatch was started.

        Args:
            None

        Returns:
            int: The elapsed time in seconds.
        """
        start = self.start_time
        time = mktime(localtime())
        delta = time - start
        return delta


class Startup:
    def __init__(self) -> None:
        """
        Initializes a Startup object.

        Args:
            None

        Returns:
            None
        """
        self.startup_done = False
        self.startup_aborted = False
        self.led = LED_Strip(25)
        self.io = Microcontroller()
        self.time = Time()
        _thread.start_new_thread(self.startup_lights, ()) # Laver fancy lys imens systemet starter op
        
        for i in range(10): # Giver 4 sek under startup til at afbryde startup med SIGINT-knappen
            print(f"Startup interrupt timer: {10-i:02d}")
            if self.io.check_SIGINT():
                sleep_ms(200)
                self.led.LED_BRIGHTNESS = 10
                self.led.led_on(self.led.red)
                self.startup_aborted = True
                print("Startup interrupted using SIGINT!")
                return None
            sleep_ms(400)
         
    def startup_lights(self):
        """
        Performs a light display during system startup.

        Args:
            None

        Returns:
            None
        """
        self.led.led_rainbow_trail(seconds=5)    

if __name__ == "__main__":
    test = Startup()
    sleep_ms(1000)
    time = Time()
    print("time:", time.rtc_fetch_unix_time())
    print("uptime:", time.get_uptime())
    io = Microcontroller()
    print("turnrate:", io.check_setting_turn_rate())
    print("wetness:", io.check_setting_wetness())
    led = LED_Strip(led_brightness=25)
    led.led_rainbow_trail(interval= 3, seconds=2)
