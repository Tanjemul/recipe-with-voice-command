from flask import Flask, jsonify, request 
import requests

from flask import Flask, request, jsonify
import whisper
import string
from pydub import AudioSegment
import os

API_BASE_URL = "https://www.themealdb.com/api/json/v1/1"

API_URL_RS = API_BASE_URL + "/filter.php"
API_URL_RD = API_BASE_URL + "/lookup.php"

API_KEY = "your_api_key_here"

# Load Whisper model
model = whisper.load_model("base")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route("/recepie-suggestion", methods = ['GET'])
def fetch_sugg():
    try:
        headers = {
            'Content-Type': 'application/json'

        }
        query_params = request.args.to_dict()

        response = requests.get(API_URL_RS, headers=headers, params=query_params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data), 200
        else:
            return jsonify({'error': 'Failed to fetch data', 'details': response.text}), response.status_code
        
    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500    
    
@app.route("/recepie-details", methods = ['GET'])
def fetch_details():
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        query_params = request.args.to_dict()

        response = requests.get(API_URL_RD, headers=headers, params=query_params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data), 200
        else:
            return jsonify({'error': 'Failed to fetch data', 'details': response.text}), response.status_code
        
    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500      



@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file part in the request"}), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"success": False, "message": "No selected file"}), 400
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Convert audio to (16 kHz, mono, WAV)
        audio = AudioSegment.from_file(file_path)
        converted_path = file_path.rsplit('.', 1)[0] + "_converted.wav"
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(converted_path, format="wav")

        # Transcribe the converted audio
        result = model.transcribe(converted_path, language="en")

        # Clean up uploaded files
        os.remove(file_path)
        os.remove(converted_path)

        text = result["text"]

        full_text = text.strip()
        cleaned_text = full_text.translate(str.maketrans('', '', string.punctuation)) 

        # Get the first word
        first_word = cleaned_text.split()[0] if cleaned_text else None

        headers = {
            'Content-Type': 'application/json'
        }
        query_params = {
            'i': first_word
        }

        response = requests.get(API_URL_RS, headers=headers, params=query_params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return jsonify({'data':data, 'cleaned_text': text}), 200
        else:
            return jsonify({'error': 'Failed to fetch data', 'details': response.text, 'full_text': text}), response.status_code
        

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500          

if __name__== '__main__':
    app.run(debug=True)
