# OCR and Semantic Search Application

This application implements two primary functionalities:
1. **OCR (Optical Character Recognition):** Extract text from uploaded images, detect the language of the text, and generate image captions.
2. **Semantic Search:** Perform searches based on semantic similarity, enabling the retrieval of relevant sentences from a body of text based on the meaning rather than exact word matching.

## Prerequisites:
 Install Python 3.8 or higher and required packages.

# Installation:
 Clone the repository and navigate into the project folder.


git clone https://github.com/your-repo/ocr-search-app.git
cd ocr-search-app

# Set up a virtual environment and activate it.
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install the required dependencies.
pip install -r requirements.txt

## Approach

### 1. OCR (Optical Character Recognition)

#### **Image Preprocessing:**
To ensure accurate text extraction from images, we use image preprocessing techniques. These steps are crucial for improving OCR performance by enhancing the visibility and sharpness of the text. The steps include:
- **Grayscale Conversion:** Converts the image to grayscale to focus on the text content.
- **Gaussian Blur:** Smoothens the image to reduce noise while preserving the structure of the text.
- **Adaptive Thresholding:** Converts the image to binary (black and white) using adaptive thresholding. This step helps highlight the text by making it stand out against the background, making it easier for the OCR model to extract characters.

These preprocessing steps ensure that the text in the image is more recognizable and easier for the OCR engine to read, especially when working with noisy or complex images.

#### **Text Extraction (EasyOCR):**
For extracting text, we use `easyocr`, a powerful OCR tool that supports multiple languages. In this application, we’ve configured EasyOCR to extract text from images in both **English** and **Hindi**. This allows for multilingual text extraction, which is especially useful when working with diverse datasets or documents that contain multiple languages.

#### **Language Detection:**
Once the text is extracted from the image, the application uses the `langdetect` library to automatically detect the language of the extracted text. This feature provides additional insights into the content of the document, allowing users to know the language in which the document is written.

#### **Image Captioning (ViT-GPT2):**
In addition to extracting text, the application can also generate captions for the images. This is done using a **Vision-Encoder-Decoder model** (`ViT-GPT2`), a pre-trained image captioning model from Hugging Face. The model analyzes the visual content of the image and generates a short description (caption) based on what it "sees". This is particularly useful in contexts where the visual content is as important as the textual content.

#### **OCR Results:**
For each uploaded image, the application returns:
- **Extracted Text:** The recognized text from the image.
- **Language:** The detected language of the extracted text.
- **Image Caption:** A generated caption that describes the visual content of the image.

### 2. Semantic Search

Semantic search allows users to find relevant information in large text documents by understanding the meaning behind the words, rather than just performing simple keyword matching. This is implemented using the `sentence-transformers` library, which provides state-of-the-art models for encoding sentences into dense vector representations.

#### **Text Embedding:**
The first step in semantic search is transforming both the **search query** and the **sentences** from the text into vector embeddings. These embeddings are high-dimensional representations that capture the semantic meaning of the sentences. This allows the search engine to compare the meaning of the query with the sentences in the text, rather than just comparing raw words.

The model used for this task is `paraphrase-MiniLM-L6-v2`, a lightweight and efficient model that provides good performance for semantic similarity tasks. Each sentence from the text is encoded into a vector, and the query is similarly transformed into a vector.

#### **Cosine Similarity:**
Once both the query and text sentences are transformed into embeddings, **cosine similarity** is used to measure the similarity between the query and each sentence in the text. Cosine similarity is a metric that calculates the cosine of the angle between two vectors in a multi-dimensional space, and it is widely used for comparing the similarity of vectorized data.

#### **Result Filtering and Ranking:**
The search results are ranked by their cosine similarity scores. Sentences that have a higher cosine similarity to the query are considered more relevant. A **minimum score threshold** is applied to filter out irrelevant or low-relevance sentences. The top `k` (configurable) most relevant sentences are returned as the final search results.

The advantage of this approach is that it can identify relevant information even if the words in the query are not an exact match to the words in the document, making it ideal for natural language search tasks.

#### **Semantic Search Results:**
For each search query, the application returns:
- **Top Matched Sentences:** Sentences from the text that have the highest semantic similarity to the query.
- **Similarity Scores:** The cosine similarity score for each matched sentence, indicating how relevant the sentence is to the query.

## Usage:
# To start the Flask server, run:
python app.py
Access the application at http://127.0.0.1:5000.

# To upload an image for OCR processing:
 Replace 'your_image.jpg' with the actual image file.
curl -X POST -F "file=@your_image.jpg" http://127.0.0.1:5000/upload

# To perform a semantic search:
 Replace 'example search query' and 'text to search from' accordingly.
curl -X POST -H "Content-Type: application/json" \
-d '{"query": "example search query", "text": "paragraph of text to search from"}' \
http://127.0.0.1:5000/search

## File Structure:
 - app.py: Main Flask application.
 - ocr.py: OCR processing logic, including text extraction, language detection, and captioning.
 - search.py: Semantic search functionality using sentence embeddings and cosine similarity.
 - templates/index.html: HTML frontend template.


