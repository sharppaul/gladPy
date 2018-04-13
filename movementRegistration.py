import RPi.GPIO as GPIO

class MovementRegistration:
    def __init__():
        PIR_PIN = 11

        GPIO.setwarnings(False)
        GPIO.setboard(GPIO.BOARD)
        GPIO.setup(PIR_PIN, GPIO.IN)
    
    @staticmethod
    def registerMovement():
        i = GPIO.input(PIR_PIN)
        if i == 1:
            print("Movement detected!")
            return True
        return False

