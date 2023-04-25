class TestError(Exception):
    "Raised when the exception is of type 'Test'"
    def __init__(self) -> None:
        super().__init__("This is an exception test")

class WiFiError(Exception):
    "Raised when something is wrong with the wifi-connection"
    def __init__(self) -> None:
        super().__init__("There was a problem with the WiFi-connection")
