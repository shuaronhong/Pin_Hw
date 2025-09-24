from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from core import extract_menu_items

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "*"}})  # Enable CORS for frontend requests

# Serve images from the images directory
@app.route('/images/<filename>')
def serve_image(filename):
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    return send_from_directory(images_dir, filename)

@app.route('/extract-menu', methods=['POST'])
def extract_menu():
    try:
        data = request.get_json()
        filename = data.get('filename')
        language = data.get('language', '英文')
        
        if not filename:
            return jsonify({'error': 'Filename is required'}), 400
        
        # Construct the full image path
        image_path = os.path.join(os.path.dirname(__file__), 'images', filename)
        
        # Check if file exists
        if not os.path.exists(image_path):
            return jsonify({'error': f'Image file {filename} not found'}), 404
        
        # Extract menu items using the existing function
        result = extract_menu_items(image_path, language)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Google Menu Translator API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
