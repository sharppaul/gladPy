import requests


class SpeechToText:
    def __init__(self):
        self.url = 'https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?language=en-us&format=simple'
        self.header = {'Ocp-Apim-Subscription-Key': '56ec29e90af041219244d3d0af5d37cf', 'Transfer-Encoding': 'chunked', 'Content-type': 'audio/wav; codec=audio/pcm; samplerate-16000'}
        self.session = requests.Session()
        self.session.headers.update(self.header)

    @staticmethod
    def read_in_chunks(fileToChunk, chunk_size=1024):
        while True:
            data = fileToChunk.read(chunk_size)
            if not data:
                break
            yield data

    def speech_to_text(self, file_name):
        with open(file_name, 'rb') as body:
            request = self.session.post(self.url, self.read_in_chunks(body))
            return request.text
