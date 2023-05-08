# Her sker der ikke noget endnu ):
from time import sleep
import device
import moisture
import rotation

MINUTES = 60
UPDATE_INTERVAL = 15 * MINUTES # Update interval in seconds, the time that is paused at the end of the loop

if __name__ == "__main__":
    
    startup = device.Startup()
    print("startup done")
    moisture = moisture.Moisture()
    rotation = rotation.Rotation()

    while True:
        # Moisture
        if moisture.too_dry():
            moisture.flash()

        #Rotation
        if rotation.is_time_to_rotate():
            rotation.rotate()
        
        print()
        sleep(UPDATE_INTERVAL)
