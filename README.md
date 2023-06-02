
# AAU-SSP-AutoPlant
This project consists of four Python modules: `main.py`, `device.py`, `moisture.py`, and `rotation.py`. These modules are used to control a device that monitors moisture levels and rotates a motor at specified intervals based on the input from the user.

## Files
* `main.py`: This is the main entry point of the program. It initializes the device and starts the moisture monitoring and rotation processes.
* `device.py`: This module contains the classes Microcontroller and LED_Strip, which handle the device`s input/output and LED functionality, respectively.
* `moisture.py`: This module contains the Moisture class, which handles the moisture sensor functionality and checks if the moisture level is too dry.
* `rotation.py`: This module contains the Motor class, which handles the motor rotation functionality and determines when it is time to rotate.


## Usage
To use this code, follow these steps:

1. Connect the necessary hardware components to your microcontroller according to the `cable-colors.png`.
2. Upload the code to your microcontroller.
3. Run the program and monitor the plant and controller.


## Dependencies
This project requires the following dependencies:

* **time module**: Used for time-related operations.
* **device module**: Contains the Microcontroller and LED_Strip classes.
* **moisture module**: Contains the Moisture class.
* **rotation module**: Contains the Motor class.


## Configuration
The behavior of the device can be configured through the following variables in the code:

* **MINUTES**: The number of minutes in an hour.
* **UPDATE_INTERVAL**: The time interval (in seconds) between each update of the device`s state.


The behavior of the LED strip can be configured through the following variables in the **LED_Strip** class:

* **LED_BRIGHTNESS**: The brightness level of the LEDs. Must be a value between 1 and 100.


The behavior of the moisture sensor can be configured through the following variables in the **Moisture** class:

* **MIN_VALUE**: The minimum value read from the moisture sensor when the pot is slightly overwatered.
* **too_dry_threshold_dry**: The moisture percentage threshold for the "dry" setting.
* **too_dry_threshold_normal**: The moisture percentage threshold for the "normal" setting.
* **too_dry_threshold_wet**: The moisture percentage threshold for the "wet" setting.


The behavior of the motor rotation can be configured through the following variables in the **Motor** class:

* **esc_data1** and **esc_data2**: The pins used for controlling the motor.
* **rotation_interval**: The interval (in weeks) at which the motor should rotate.


## License

This project is licensed under the [MIT License](LICENSE).
