from time import sleep
import device
import moisture
import rotation

MINUTES = 60
UPDATE_INTERVAL = 10 #*MINUTS 

if __name__ == "__main__": 
    """Main entry point of the script."""
    startup = device.Startup()
    print("Startup done")
    moisture = moisture.Moisture()
    rotation = rotation.Step_Motor()
    if not startup.startup_aborted: startup.led.led_on_single(43, startup.led.green)

    while not startup.startup_aborted:
        
        # Moisture
        if moisture.too_dry():
            moisture.flash()
        
        startup.led.led_on_single(43, startup.led.green)

        #Rotation
        if rotation.is_time_to_rotate():
            rotation.rotate()
        
        print("sleeping for", UPDATE_INTERVAL, "seconds")
        sleep(UPDATE_INTERVAL)
