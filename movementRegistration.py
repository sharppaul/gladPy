import RPi.GPIO as GPIO


class MovementRegistration:
    def __init__(self):
        self.PIR_PIN = 10

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIR_PIN, GPIO.IN)

    def registerMovement(self):
        i = GPIO.input(self.PIR_PIN)
        if i == 1:
            print("Movement detected!")
            return True
        return False
