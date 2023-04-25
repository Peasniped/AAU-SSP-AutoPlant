from socket import socket, AF_INET, SOCK_DGRAM, getaddrinfo
from struct import unpack
from network import WLAN, STA_IF
from time import gmtime, mktime, sleep_ms, localtime
from machine import RTC, Pin, reset
from neopixel import NeoPixel
from os import listdir
import _thread
from custom_exceptions import *

class IO:
    def __init__(self) -> None:
        self.input_SIGINT = Pin(15, Pin.IN, Pin.PULL_DOWN)
        self.input_2wk = Pin(13, Pin.IN, Pin.PULL_DOWN)
        self.input_6wk = Pin(14, Pin.IN, Pin.PULL_DOWN)
        self.input_dry = Pin(0, Pin.IN, Pin.PULL_DOWN)
        self.input_wet = Pin(1, Pin.IN, Pin.PULL_DOWN)

    def check_SIGINT(self) -> bool:
        if self.input_SIGINT.value() == 1:
            return True
        else: return False
    
    def check_setting_wetness(self) -> str:
        if self.input_wet.value() == 1:
            return "wet"
        elif self.input_wet.value() == 0 and self.input_dry.value() == 0:
            return "normal"
        elif self.input_dry.value() == 1:
            return "dry"
        
    def check_setting_turn_rate(self) -> int:
        if self.input_2wk.value() == 1:
            return 2
        elif self.input_2wk.value() == 0 and self.input_6wk.value() == 0:
            return 4
        elif self.input_6wk.value() == 1:
            return 6  



class LED(IO):

    def __init__(self, led_brightness:int = 25) -> None:
        super().__init__()

        self.LED_PIXELS = 40
        self.LED_BRIGHTNESS = led_brightness # Sættes ved instantiering af objektet - Værdi mellem 1 og 100, hvor 100 er mest lys og 1 er næsten ingen lys

        self.led_strip = NeoPixel(Pin(16), self.LED_PIXELS)

        ### COLORS (R,G,B)
        self.white = (255, 255, 255)
        self.blue = (0, 10, 255)
        self.red = (255, 5, 0)
        self.yellow = (255, 125, 0)
        self.orange = (255, 50, 0)
        self.green = (0, 255, 5)
        self.purple = (75, 0, 120)

        self.wave_stop = False
        self.trail_stop = False

    def hue_to_rgb(self, angle:int) -> tuple:
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
        LED_R = int((color[0] / 100) * self.LED_BRIGHTNESS)
        LED_G = int((color[1] / 100) * self.LED_BRIGHTNESS)
        LED_B = int((color[2] / 100) * self.LED_BRIGHTNESS)

        for i in range(self.LED_PIXELS):
            self.led_strip[i] = (LED_R, LED_G, LED_B)
        self.led_strip.write()

    def led_on_single(self, pixel:int, color:tuple, write:bool = True) -> None:
        LED_R = int((color[0] / 100) * self.LED_BRIGHTNESS)
        LED_G = int((color[1] / 100) * self.LED_BRIGHTNESS)
        LED_B = int((color[2] / 100) * self.LED_BRIGHTNESS)

        self.led_strip[pixel] = (LED_R, LED_G, LED_B)
        if write: self.led_strip.write()

    def led_off(self) -> None:
        for i in range(self.LED_PIXELS):
            self.led_strip[i] = (0, 0, 0)
        self.led_strip.write()

    def led_on_two_colors(self, color1:tuple, color2:tuple = (0,0,0)) -> None:
        LED_R1 = int((color1[0] / 100) * self.LED_BRIGHTNESS)
        LED_G1 = int((color1[1] / 100) * self.LED_BRIGHTNESS)
        LED_B1 = int((color1[2] / 100) * self.LED_BRIGHTNESS)

        LED_R2 = int((color2[0] / 100) * self.LED_BRIGHTNESS)
        LED_G2 = int((color2[1] / 100) * self.LED_BRIGHTNESS)
        LED_B2 = int((color2[2] / 100) * self.LED_BRIGHTNESS)

        for i in range(self.LED_PIXELS):
            if not i % 2 == 0:
                self.led_strip[i] = (LED_R1, LED_G1, LED_B1)
            else:
                self.led_strip[i] = (LED_R2, LED_G2, LED_B2)
        self.led_strip.write()

    def led_flash(self, flashes:int = 1, on_time_ms:int = 350, off_time_ms:int = 150, color:tuple = (0,0,0)) -> None:
        if color == (0,0,0):
            color = self.blue
        for i in range(flashes):
            self.led_on(color)
            sleep_ms(on_time_ms)
            self.led_off()
            if not i + 1 == flashes:
                sleep_ms(off_time_ms)
            

    def led_flash_double(self, flashes:int = 1, on_time_ms:int = 50, delay_time_ms:int = 75, off_time_ms:int = 2000, color:tuple = (0,0,0)) -> None:
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

    def led_color_cycle(self, cycles:int = 1, on_time_ms:int = 250) -> None:
        colors = [self.red, self.green, self. yellow, self.blue, self.orange, self. purple]
        for i in range(cycles):
            for color in colors:
                self.led_on(color)
                sleep_ms(on_time_ms)
        self.led_off()

    def led_rainbow_trail(self, interval:int = 20, trail_length:int = 25) -> None:
        self.trail_stop = False
        angle = 1
        led = 0
        direction = 1
        while self.trail_stop == False:
            color = self.hue_to_rgb(angle)
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
        self.led_off()        

    def led_color_wave(self, step:int = 1) -> None:
        self.wave_stop = False
        angle = 0
        direction = 1
        while self.wave_stop == False:
            color = self.hue_to_rgb(angle)
            self.led_on(color)
            angle += step * direction
            if angle >= 255:
                direction = -1
            elif angle <= 0:
                direction = 1
            print(angle)
        self.led_off()


class Time:

    def __init__(self) -> None:
        self.files = Files()
        self.wifi = WiFi()

        self.NTP_EPOCH = 2208988800 # 1970-01-01 00:00:00
        self.NTP_QUERY = b"\x23" + (47 * b"\0") # https://stackoverflow.com/a/26938508

    def ntp_fetch_unix_time(self, host:str = "pool.ntp.org", port:int = 123) -> int:
        ### Inspiration fra
        # https://stackoverflow.com/a/33436061
        sockaddr = getaddrinfo(host, port)[0][-1]
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(1.0)
        msg = None
        while msg == None: # <------------------------------------------------------------------------------------------- #TODO - Noget med at den skal time ud efter et minut
        
            try: 
                sock.sendto(self.NTP_QUERY, sockaddr)
                print("NTP query sent - waiting 1s for response") # <---------------------------------------------------- #DEBUG
                msg, address = sock.recvfrom(1024)
            except OSError:
                print("Timeout waiting for UDP-package!") # <------------------------------------------------------------ #DEBUG
        sock.close()
        value = unpack("!I", msg[40:44])[0]
        time = int(value - self.NTP_EPOCH)
        return time
    
    def read_timezone(self) -> tuple:
        settings = self.files.read_settings()
        try:
            timezone = int(settings["timezone"])
            tz_expiry = int(settings["tz_expiry"])
            return(timezone, tz_expiry)
        except KeyError:
            return(None, None)
        except TypeError:
            return(None, None)

    def check_timezone(self, current_unixtime:int) -> int:
        timezone, tz_expiry = self.read_timezone()
        if (timezone == None or tz_expiry == None) or current_unixtime > tz_expiry:
            print("Fetching new timezone-data") # <---------------------------------------------------------------------- #DEBUG
            timezone, tz_expiry = self.get_timezone()
            self.files.write_settings({"tz_expiry":tz_expiry})
            self.files.write_settings({"timezone":timezone})
        else:
            print(f"timezone '{timezone}' fetched from settings - Expires {self.format_time(gmtime(tz_expiry))}") # <---- #DEBUG
        return timezone
    
    def apply_timezone(self, unix_time_utc:int) -> int:
        timezone = self.check_timezone(unix_time_utc)
        time = unix_time_utc + (timezone * 3600)
        return time

    def time_now(self) -> tuple:
        """
        Returns time in tuple: ((Year, Month, Day, Hour, Minute, Second, Weekday, Day_in_year), unixtime)
                      Example: ((2023, 4, 10, 17, 53, 34, 0, 100), 1681149214)
        """
        unixtime_utc = self.ntp_fetch_unix_time()
        unixtime = self.apply_timezone(unixtime_utc)
        time = gmtime(int(unixtime))
        return (time, unixtime)

    def get_timezone(self) -> tuple:
        # Sommertid (UTC+2) starter den sidste søndag i marts
        # Normaltid (UTC+1) starter den sidste søndag i oktober
        now_unix = self.ntp_fetch_unix_time()
        time_tuple = gmtime(int(now_unix))
        
        def strip_time_from_unix(unix_time:int) -> int:
            hours = gmtime(unix_time)[3] * 3600
            minutes = gmtime(unix_time)[4] * 60
            seconds = gmtime(unix_time)[5]
            return unix_time - (hours + minutes + seconds)

        last_sunday_march = 0
        last_sunday_october = 0
        now_date = strip_time_from_unix(int(now_unix))
        day = 3600 * 24

        for counter in range(365):
            time = int(now_date + counter * day)
            time_tuple = gmtime(time)
            if time_tuple[1] == 3 and time_tuple[6] == 6:
                last_sunday_march = time
            elif time_tuple[1] == 10 and time_tuple[6] == 6:
                last_sunday_october = time
        next_summertime = last_sunday_march
        next_normaltime = last_sunday_october

        if next_summertime < next_normaltime:
            return (1, next_summertime) # Format: (Tidszone nu (UTC+#), Næste skift)
        else:
            return (2, next_normaltime) # Format: (Tidszone nu (UTC+#), Næste skift)

    def set_RTC(self, time_tuple:tuple) -> None:
        RTC().datetime((time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[6], time_tuple[3], time_tuple[4], time_tuple[5], 0))

    def format_time(self, time_tuple:tuple) -> str:
        time = f"{time_tuple[0]}-{time_tuple[1]:02d}-{time_tuple[2]:02d} {time_tuple[3]:02d}:{time_tuple[4]:02d}:{time_tuple[5]:02d}"
        return time
    

class Stopwatch:
    
    def __init__(self) -> None:
        self.start_time = mktime(localtime())
        self.lap_times = []
    
    def get_time(self) -> int:
        start = self.start_time
        time = mktime(localtime())
        delta = time - start
        return delta
    
    def lap(self) -> None:
        time = self.get_time()
        self.lap_times.append(time)

    def last_lap(self) -> int:
        last_lap = self.lap_times[-1]
        return last_lap    

    def time_delta_last_lap(self) -> int:
        time = self.get_time()
        last_lap = self.last_lap()
        return time - last_lap


class WiFi:
    
    def __init__(self) -> None:
        self.default_ssid = "some_ssid" # <------------------------------------------------------------------------------ Default Wi-Fi SSID sættes her
        self.default_pass = "some_pass" # <------------------------------------------------------------------------------ Default Wi-Fi pass sættes her
        self.wlan = WLAN(STA_IF)
        pass

    def connect(self, ssid:str = "", password:str = "", timeout:int = 5, tries:int = 3) -> None:
        for i in range(tries):
            stopwatch = Stopwatch()
            if ssid == "" or password == "":
                ssid = self.default_ssid
                password = self.default_pass
            
            self.wlan.active(True)
            self.wlan.connect(ssid, password)
            while self.wlan.isconnected() == False:
                if stopwatch.get_time() >= timeout: break # Timeout
                print('Waiting for Wi-Fi connection...', stopwatch.get_time())
                sleep_ms(1000)
            if self.wlan.isconnected() == True:
                print(self.wlan.ifconfig())
                break
            else:
                print(f"Failed to connect to WiFi on try {i+1} of {tries}")
        if self.wlan.isconnected() == False:
            raise WiFiError

    def check_connection(self):
        if self.wlan.isconnected() == True:
            return True
        else:
            return False
    
    def disconnect(self):
        self.wlan.active(False)

    # <------------------------------------------------------------------------------------------------------------------ #TODO        
    # Metode der lav WiFi-hotspot som man kan connecte til
    # Når man connecter bliver man redirectet til en side i browser (ala net.aau.dk og alle andre pay-to-access-wifi)
    # her vises resultatet fra en WiFi-scan. Man kan vælge et SSID og skrive en kode
    # Der forsøges at forbinde, hvis der er success gemmes SSID og password i settings-fil
    # Hvis der ikke er success vises en fejlmeddelse og der laves et nyt scan som vises på siden.


class Files:

    def __init__(self) -> None:
        self.SETTINGS_FILE = "settings.file"

    def read_settings(self) -> dict:
        try:
            if not self.SETTINGS_FILE in listdir():
                raise NameError("File does not exist")            
            file = open(self.SETTINGS_FILE,"r")
            contents = file.read()
            settings_dict = {}
            contents = contents.strip(",")
            for kv in contents.split(","):
                if kv == "None:None":
                    pass
                else:
                    #print(f"kv = {kv}") # <------------------------------------------------------------------------------- #DEBUG
                    key, value = kv.split(":")
                    settings_dict[key] = value
            file.close()
            return settings_dict
        except Exception as e:
            print(f"some failure happened - {e}")# <----------------------------------------------------------------------- #DEBUG
            file = open(self.SETTINGS_FILE,"w")
            file.close()
            return {None:None}
    
    def write_settings(self, new_settings_dict:dict) -> None:
        settings_dict = self.read_settings()
        settings_dict.update(new_settings_dict)
        settings_str = ""
        file = open(self.SETTINGS_FILE,"w")
        for each in settings_dict:
            settings_str += f"{each}:{settings_dict[each]},"
        file.write(settings_str)
        file.close()


class Startup:

    def __init__(self) -> None:
        self.startup_done = False
        self.led = LED(25)
        self.io = IO()
        self.wifi = WiFi()
        self.files = Files()
        self.time = Time()
        
        # Laver fancy lys imens systemet starter op
        _thread.start_new_thread(self.wait_for_startup, ())
        
        for i in range(10): # Giver 2 sek under startup til at afbryde startup med SIGINT-knappen
            print(f"Startup interrupt timer: {10-i:02d}")
            if self.io.check_SIGINT():
                self.startup_done = True
                self.led.trail_stop = True
                sleep_ms(200)
                self.led.LED_BRIGHTNESS = 10
                self.led.led_on(self.led.red)
                print("Startup interrupted using SIGINT!")
                return
            sleep_ms(200)

        # Starter startup-sekvensen og holder øje med fejl
        try:
            self.startup_seq()
        except WiFiError as e:
            self.startup_done = True
            print(e, "\nRestarting device")
            self.led.led_flash_double(4, color=self.led.red)
            # Device reset
            reset()
        except:
            print("something something")
            self.startup_done = True

    def wait_for_startup(self):
        while not self.startup_done:
            self.led.led_rainbow_trail()
         

    def startup_seq(self):
        settings = self.files.read_settings()
        try:
            # Hvis der er wifi-credentials: connect
            ssid = settings["wifi_ssid"]
            password = settings["wifi_password"]
            self.wifi.connect(ssid, password)
        except KeyError as e:
            # ellers kør metode til at vælge sside og skrive password ind
            print("no WiFi login is stored in settings! - Starting login page")
            self.wifi.connect() # Indtil metoden med login er lavet køres denne, her bruges default credentials som defineres i WiFi.__init__()
        
        time = self.time.time_now()[0]
        self.time.set_RTC(time)

        self.startup_done = True
        self.led.trail_stop = True

class Demo:

    def __init__(self) -> None:
        self.led = LED(led_brightness=40)
        self.io = IO()
        pass

    def setting_selection(self) -> None:
        while not self.io.check_SIGINT():
            if io.check_setting_wetness() == "wet":
                color = led.blue
            elif io.check_setting_wetness() == "normal":
                color = (0,0,0)
            elif io.check_setting_wetness() == "dry":
                color = led.purple
            
            if io.check_setting_turn_rate() == 2:
                color2 = led.green
            elif io.check_setting_turn_rate() == 4:
                color2 = (0,0,0)
            elif io.check_setting_turn_rate() == 6:
                color2 = led.orange
            
            led.led_on_two_colors(color, color2)
        led.led_off()


if __name__ == "__main__":
    led = LED(led_brightness=10)
    io = IO()
    demo = Demo()
    _thread.start_new_thread(led.led_rainbow_trail, ())
    sleep_ms(3000)
    led.trail_stop = True

    demo.setting_selection()

    #wifi = WiFi()

    #startup = Startup()
    #sleep_ms(3000)
    #led.led_flash(color=led.green)

    #wifi = WiFi()
    #wifi.connect(tries=1, timeout=5)
    #print("Wi-Fi Connected:", wifi.check_connection())
