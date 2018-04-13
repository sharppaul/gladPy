from subprocess import call

if __name__ == '__main__':
    while True:
        try:
            call(["python3", "speechRecognitionTest.py"])
        except FileNotFoundError:
            call(["python", "speechRecognitionTest.py"])