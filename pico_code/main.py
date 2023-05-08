# Her sker der ikke noget endnu ):
import device
import moisture
import rotation

if __name__ == "__main__":
    def pseudo_rotate():
        startup.led.led_rainbow_trail(seconds=5)
        print("rotation done")
    
    startup = device.Startup()
    print("startup done")
    moisture = moisture.Moisture()

    while True:
        # Moisture
        if moisture.too_dry():
            moisture.flash()

        #Rotation
        if rotation.time_to_rotate():
            pseudo_rotate()
