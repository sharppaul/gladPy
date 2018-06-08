import sounddevice as sd
import soundfile as sf
from math import sqrt
from math import log10
import numpy as np
from time import time


class SoundRecorder:
    def __init__(self):
        self.duur = 4  # Duur van de opname
        self.samplerate = sd.default.samplerate = 16000  # Sample rate
        self.channels = sd.default.channels = 1  # mono geluid
        self.minimal_volume = -50  # Default minimal volume

    def volume_test_recording(self):
        volumeTestRecording = sd.rec(self.samplerate)  # Records one second
        sd.wait()                                       # Waits till recording is done
        return volumeTestRecording

    @staticmethod
    def play(file):
        data, samplerate = sf.read(file)    # read WAV file
        sd.play(data, samplerate)           # play it
        sd.wait()                           # wait till done

    @staticmethod
    def calculate_volume_rms(recording):
        rms = sqrt(sum([pow(sample, 2) for sample in recording]) / len(recording))  # gemiddeld volume berekening
        return 20 * log10(rms)

    def continue_recording_and_write_to_file(self, initial_recording):
        recording = sd.rec(self.duur * self.samplerate)         # record 4 seconds
        sd.wait()                                               # wait till done recording
        recording = np.append(initial_recording, recording)     # append previous recording to new one
        file_name = "wav/" + str(round(time())) + '.wav'        # save .wav file
        sf.write(file_name, recording, self.samplerate)
        return file_name                                        # return the file name

    def set_base_volume(self):
        """Record a sample and calculate the average volume. Expects the sample to be ambient noise in the room."""
        test_recording = self.volume_test_recording()
        dB = self.calculate_volume_rms(test_recording)
        print("Registered volume: " + str(dB))
        dB += 5
        print("Setting treshold: " + str(dB))
        self.minimal_volume = dB

    def test_and_record(self):
        """Tests for 1 second, if above ambient volume, then records for 4 additional seconds."""
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
