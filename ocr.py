
import easyocr
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
import cv2
import numpy as np
from PIL import Image
from langdetect import detect

class AdvancedOCRProcessor:
    def __init__(self):
        # Initialize models for OCR and image captioning
        self.reader = easyocr.Reader(['en', 'hi'])  # For English and Hindi languages
        self.image_captioner = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.image_captioner.to(self.device)

    def preprocess_image(self, image):
        """Preprocess the image to improve OCR results."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return thresh

    def generate_caption(self, image):
        """Generate a caption for the input image using ViT-GPT2."""
        pixel_values = self.feature_extractor(images=[image], return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)
        output_ids = self.image_captioner.generate(pixel_values, max_length=16, num_beams=4)
        preds = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        return preds[0].strip()

    def detect_language(self, text):
        """Detect the language of the extracted text."""
        try:
            return detect(text)
        except:
            return "unknown"

    def process_image(self, image_file):
        """Process the uploaded image to extract text, detect language, and generate captions."""
        try:
            image = Image.open(image_file).convert('RGB')
            image_np = np.array(image)
            preprocessed_image = self.preprocess_image(image_np)

            # Use EasyOCR to extract text
            ocr_result = self.reader.readtext(preprocessed_image, detail=0)
            ocr_text = " ".join(ocr_result)

            # Detect language in extracted text
            lang = self.detect_language(ocr_text)

            # Generate image caption
            caption = self.generate_caption(image)

            return {
                "ocr_text": ocr_text,
                "language": lang,
                "caption": caption
            }
        except Exception as e:
            return {"error": str(e)}
