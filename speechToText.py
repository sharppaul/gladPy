import requests


class SpeechToText:
    def __init__(self):
        """Microsoft bing API URL, headers etc. also creates a new HTTP session"""
        self.url = 'https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?language=en-us&format=simple'
        self.header = {'Ocp-Apim-Subscription-Key': '56ec29e90af041219244d3d0af5d37cf', 'Transfer-Encoding': 'chunked', 'Content-type': 'audio/wav; codec=audio/pcm; samplerate-16000'}
        self.session = requests.Session() # create HTTP session
        self.session.headers.update(self.header) # set headers.

    @staticmethod
    def read_in_chunks(fileToChunk, chunk_size=1024):
        """Reads file in chunks and yields a chunk with size chunk_size (default 1024 byte)"""
        while True:
            data = fileToChunk.read(chunk_size)
            if not data:
                break
            yield data

    def speech_to_text(self, file_name):
        """
        Makes a request to the microsoft API with the WAV file data in the body.
        Returns the object with data that MS recognized.
        """
        with open(file_name, 'rb') as body:
            request = self.session.post(self.url, self.read_in_chunks(body))
            return request.text
