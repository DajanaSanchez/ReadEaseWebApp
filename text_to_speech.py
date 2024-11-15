from gtts import gTTS
import os

class TextToSpeech:
    def __init__(self, rate=150):
        # Default TTS rate (words per minute); not used in gTTS
        self.rate = rate

    def read_text(self, text):
        """Convert the extracted text to speech and save as an audio file."""
        try:
            tts = gTTS(text=text, lang='en', slow=True)  # Slow speech
            tts_path = "text_audio.mp3"
            tts.save(tts_path)
            return tts_path
        except Exception as e:
            return f"Error generating speech: {e}"

# Example usage
if __name__ == "__main__":
    tts = TextToSpeech()
    audio_file = tts.read_text("Hello, this is a text to speech test.")
    if not audio_file.startswith("Error"):
        print(f"Audio saved to {audio_file}")
    else:
        print(audio_file)
