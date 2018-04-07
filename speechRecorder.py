import sounddevice as sd
import soundfile as sf
from math import sqrt
from math import log10
import numpy as np
from time import time


class SoundRecorder:
    def __init__(self):
        self.duur = 4
        self.samplerate = sd.default.samplerate = 16000
        self.channels = sd.default.channels = 1
        self.minimal_volume = -50

    def volume_test_recording(self):
        volumeTestRecording = sd.rec(self.samplerate)
        sd.wait()
        return volumeTestRecording

    @staticmethod
    def play(file):
        data, samplerate = sf.read(file)
        sd.play(data, samplerate)
        sd.wait()

    @staticmethod
    def calculate_volume_rms(recording):
        rms = sqrt(sum([pow(sample, 2) for sample in recording]) / len(recording))
        return 20 * log10(rms)

    def continue_recording_and_write_to_file(self, initial_recording):
        recording = sd.rec(self.duur * self.samplerate)
        sd.wait()
        recording = np.append(initial_recording, recording)
        file_name = "wav/" + str(round(time())) + '.wav'
        sf.write(file_name, recording, self.samplerate)
        return file_name

    def set_base_volume(self):
        test_recording = self.volume_test_recording()
        dB = self.calculate_volume_rms(test_recording)
        print("Registered volume: " + str(dB))
        dB += 5
        print("Setting treshold: " + str(dB))
        self.minimal_volume = dB

    def test_and_record(self):
        test_recording = self.volume_test_recording()
        dB = self.calculate_volume_rms(test_recording)
        if dB > self.minimal_volume:
            return self.continue_recording_and_write_to_file(test_recording)
        else:
            return None

    @staticmethod
    def print_info():
        print(sd.default.device)


if __name__ == "__main__":
    recorder = SoundRecorder()
    recorder.set_base_volume()

    while True:
        print(recorder.test_and_record())
