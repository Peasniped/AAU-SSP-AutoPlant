class CustomError(Exception):
    "Raised when the exception is of type CustomError"
    def __init__(self) -> None:
        super().__init__("This is a custom exception")

class WiFiError(Exception):
    "Raised when something is wrong with the wifi-connection"
    def __init__(self) -> None:
        super().__init__("There was a problem with the WiFi-connection")