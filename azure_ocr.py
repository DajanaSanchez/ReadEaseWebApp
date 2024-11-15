#handles the Azure OCR functionality
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os


class AzureOCR:
    def __init__(self, subscription_key, endpoint):
        self.client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    def perform_ocr(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                ocr_result = self.client.read_in_stream(image_file, raw=True)
                operation_id = ocr_result.headers["Operation-Location"].split("/")[-1]

                # Wait for the OCR operation to complete
                while True:
                    ocr_result = self.client.get_read_result(operation_id)
                    if ocr_result.status not in ['notStarted', 'running']:
                        break

                recognized_text = ""
                if ocr_result.status == 'succeeded':
                    for page in ocr_result.analyze_result.read_results:
                        for line in page.lines:
                            recognized_text += line.text + "\n"
                return recognized_text

        except Exception as e:
            return f"Error performing OCR: {e}"
