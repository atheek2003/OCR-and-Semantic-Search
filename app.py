
from flask import Flask, request, jsonify, render_template
from ocr import AdvancedOCRProcessor
from search import SemanticSearch

# Initialize OCR processor and semantic search engine
ocr_processor = AdvancedOCRProcessor()
search_engine = SemanticSearch()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Process the image for OCR, language detection, and captioning
    try:
        result = ocr_processor.process_image(file)
        if "error" in result:
            return jsonify({"error": result["error"]}), 500
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    text = data.get('text')
    
    if not query or not text:
        return jsonify({'error': 'Query or text not provided'}), 400
    
    try:
        results = search_engine.semantic_search(query, text)
        if "error" in results:
            return jsonify({"error": results["error"]}), 500
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
