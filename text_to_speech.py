import os
from kivy.utils import platform

class TextToSpeech:
    def __init__(self, rate=150):
        # Default TTS rate (words per minute); 125 is slower than the default (200)
        self.rate = rate

    def read_text(self, text):
        """Convert the extracted text to speech based on the platform."""
        if platform == "android":
            # Slow down speech with gTTS by setting the `slow` parameter to True
            from gtts import gTTS
            from jnius import autoclass

            tts = gTTS(text=text, lang='en', slow=True)  # Slow speech
            tts_path = "text_audio.mp3"
            tts.save(tts_path)

            MediaPlayer = autoclass("android.media.MediaPlayer")
            media_player = MediaPlayer()
            media_player.setDataSource(tts_path)
            media_player.prepare()
            media_player.start()
        else:
            # Use pyttsx3 for iOS and macOS
            import pyttsx3
            engine = pyttsx3.init()

            # Set the speech rate to slow it down
            engine.setProperty("rate", self.rate)

            # Read the text aloud
            engine.say(text)
            engine.runAndWait()