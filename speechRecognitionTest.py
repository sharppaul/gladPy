from speechToText import *
from speechRecorder import *
from classes import *
import os
import json
import random
import time

recorder = SoundRecorder()
stt = SpeechToText()
wthr = WeatherGrabber()

TURRET_SOUND_FILES = "soundfiles/turrets"
GLADOS_SOUND_FILES = "soundfiles/glados"
SONGS_SOUND_FILES = "soundfiles/songs"
KEYWORD = " "
CITY = 'Rotterdam'

timeKeywords = ['what', 'time']
dateKeywords = ['what', 'date']
weatherKeywords = ['what', 'weather']
weatherKeywords2 = ['how', 'weather']
thankyouKeywords = ['thank', 'you']
playsongKeywords = ['play', 'song']

weather = wthr.get_current_weather(CITY)


def test(line, keywords, functionname):
    for word in keywords:
        if word not in line:
            return False

    if functionname in globals():
        globals()[functionname]()
    elif functionname in locals():
        locals()[functionname]()
    else:
        return False

    return True


def playPortalSong():
    file = SONGS_SOUND_FILES + '/' + random.choice(os.listdir(SONGS_SOUND_FILES))
    recorder.play(file)


def randomTurretNoise():
    file = TURRET_SOUND_FILES + '/' + random.choice(os.listdir(TURRET_SOUND_FILES))
    recorder.play(file)


def pronounce_number_string(string, leading_zero=True):
    for i in string:
        if leading_zero and i == '0':
            pass
        else:
            recorder.play(GLADOS_SOUND_FILES + '/number_{}.wav'.format(i))
            time.sleep(0.12)
        leading_zero = False


def thank_you():
    recorder.play(GLADOS_SOUND_FILES + '/thanks_for_nothing.wav')


def tell_date():
    t = time.strftime('Today is  %m day %d')
    recorder.play(GLADOS_SOUND_FILES + '/today_is.wav')
    time.sleep(0.2)
    pronounce_number_string(time.strftime('%m'))
    time.sleep(0.3)
    pronounce_number_string(time.strftime('%d'))
    print(t)


def tell_time():
    t = time.strftime('It is %I %M %p')
    recorder.play(GLADOS_SOUND_FILES + '/it_is.wav')
    time.sleep(0.1)
    pronounce_number_string(time.strftime('%I'))
    time.sleep(0.3)
    pronounce_number_string(time.strftime('%M'), leading_zero=False)
    print(t)


def tell_weather():
    global weather
    weather = wthr.get_current_weather(CITY)
    print(weather)


def command(line):
    line = line.lower()
    if KEYWORD in line:
        has_executed = False

        """Time telling"""
        has_executed = has_executed or test(line, timeKeywords, 'tell_time')

        """Date telling"""
        has_executed = has_executed or test(line, dateKeywords, 'tell_date')

        """Weather telling"""
        has_executed = has_executed or test(line, weatherKeywords, 'tell_weather')
        has_executed = has_executed or test(line, weatherKeywords2, 'tell_weather')

        """Play song"""
        has_executed = has_executed or test(line, thankyouKeywords, 'thank_you')

        """Thank you"""
        has_executed = has_executed or test(line, playsongKeywords, 'playPortalSong')

        if not has_executed:
            randomTurretNoise()
    else:
        randomTurretNoise()


def main():
    recorder.set_base_volume()
    running = True
    while running:
        recordedFile = None
        while recordedFile is None:
            recordedFile = recorder.test_and_record()
            if recordedFile is None:
                print("Couldn't hear anything!")
            else:
                print("Heard {}".format(recordedFile))

        result = stt.speech_to_text(recordedFile)

        jsonFile = json.loads(result)
        resultText = None
        if jsonFile['RecognitionStatus'] == 'Success':
            resultText = jsonFile['DisplayText']
        else:
            print("I'm sorry, can you repeat that? \t ErrorCode: " + jsonFile['RecognitionStatus'])
            randomTurretNoise()

        if resultText is not None:
            print(resultText)
            command(resultText)

        os.remove(recordedFile)


if __name__ == '__main__':
    main()
