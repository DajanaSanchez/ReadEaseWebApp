from flask import Flask, render_template, request, jsonify
from azure_ocr import AzureOCR
from text_to_speech import TextToSpeech
import base64
import io
from PIL import Image
import tempfile
from gtts import gTTS
import os

app = Flask(__name__)

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image processing via OCR
@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Get the image data from the POST request
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        # Decode the base64 image data
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_bytes))

        # Save the image temporarily to process with OCR
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
            image.save(temp_image.name)

            # Perform OCR using Azure
            azure_ocr = AzureOCR(
                subscription_key="Eljnm4KSifKb44hjsElHtEkPf2S3mJkhItXzP3naNvqHtBKn18K9JQQJ99AKACYeBjFXJ3w3AAAFACOGM7XW",
                endpoint="https://readease.cognitiveservices.azure.com/"
            )
            extracted_text = azure_ocr.perform_ocr(temp_image.name)

        return jsonify({"extracted_text": extracted_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to handle text-to-speech
@app.route('/read_text', methods=['POST'])
def read_text():
    try:
        text = request.json.get('text')
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Use gTTS to generate the audio
        tts = gTTS(text=text, lang='en')
        audio_path = "static/extracted_text.mp3"
        tts.save(audio_path)

        # Return the path to the generated audio file
        return jsonify({"audio_path": f"/{audio_path}"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
