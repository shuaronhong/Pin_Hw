# Google Menu Translator

A Vue.js frontend application that integrates with a Python backend to extract and translate menu items from images using OpenAI's GPT models.

## Features

- 📸 Upload menu images by filename
- 🤖 AI-powered menu item extraction and translation
- 🍽️ Expandable menu items with detailed ingredients and preparation methods
- 📱 Responsive design with modern UI
- 🔄 Real-time processing with loading states

## Project Structure

```
Google_Menu/
├── back_end/
│   ├── app.py              # Flask API server
│   ├── core.py             # Menu extraction logic
│   ├── config.py           # Configuration
│   ├── images/             # Menu images directory
│   ├── menu_json/          # Extracted menu JSON files
│   └── requirements.txt    # Python dependencies
├── front_end/
│   ├── src/
│   │   ├── App.vue         # Main Vue component
│   │   ├── main.js         # Vue app entry point
│   │   ├── style.css       # Global styles
│   │   └── services/
│   │       └── api.js      # API service
│   ├── index.html          # HTML template
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd back_end
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure you have your OpenAI API key set up in `openAI_API_KEY.txt`

4. Start the Flask server:
   ```bash
   python app.py
   ```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd front_end
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will run on `http://localhost:3000`

## Usage

1. Place your menu images in the `back_end/images/` directory
2. Open the frontend application in your browser
3. Enter the filename of your menu image (e.g., `Snipaste_14.png`)
4. Click "Translate Menu" to process the image
5. View the extracted menu items with translations, ingredients, and preparation details
6. Click on any menu item to expand and see detailed information

## API Endpoints

- `POST /extract-menu` - Extract menu items from an image
- `GET /images/<filename>` - Serve menu images
- `GET /health` - Health check endpoint

## Example Menu JSON Format

The extracted menu items follow this structure:

```json
{
  "菜品名称原文": {
    "translated_name": "Translated Name",
    "ingredients_and_seasonings": ["ingredient1", "ingredient2"],
    "flavor_and_preparation": "Description of taste and preparation method"
  }
}
```

## Technologies Used

- **Frontend**: Vue.js 3, Vite, Axios
- **Backend**: Flask, OpenAI GPT API
- **Styling**: CSS3 with modern gradients and animations
- **Image Processing**: Base64 encoding for OpenAI API
