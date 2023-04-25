from machine import Pin
from neopixel import NeoPixel

# Miniscript til at slukke LED-ring

LED_PIXELS = 144
led_strip = NeoPixel(Pin(16), LED_PIXELS)

def led_off() -> None:
    for i in range(LED_PIXELS):
        led_strip[i] = (0, 0, 0)
    led_strip.write()

led_off()
