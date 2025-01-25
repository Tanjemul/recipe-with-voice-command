# Recipe with Voice Command
The idea of this app is to demonstrate voice to text and using that text generating recipes instantly for the user. Working on this concept, only the backend has been implemented using python Flask. Machine lerning model [Whisper](https://github.com/openai/whisper) is used in the project to work with ffmpeg. For recipe suggestions and details, third party [The MealDB](https://www.themealdb.com/) is uded.

### Features

- Voice to text convertion
- Generating recipe list suggestion based on the voice.
- Generating recipe details

### Tech Stack
- Python 3.12.8
- flask 2.3.2
- pytorch 2.0.1  
- torchvision 0.15.2
- torchaudio 2.0.2
- openai-whisper 20230314
- pydub 0.25.1
- ffmpeg-python 0.2.0

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Tanjemul/recipe-with-voice-command.git

2. Navigate to the project directory: cd \recipe-with-voice-main

3. Install dependencies:
    ```bash
    pip install flask
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    pip install openai-whisper pydub
    pip install pydub

On your local machine, install [ffmpeg](https://ffmpeg.org/download.html)

4. Run the project
    ```bash
    set FLASK_APP=app
    flask run
On local machine, open browser and go to: http://127.0.0.1:5000

4. API Documentation:
   Only one end point is enough for this project:

   ```bash
   curl --location 'http://localhost:5000/transcribe' \
   --form 'file=@"/C:/Users/User_Name/Downloads/audio_file.mp3"'
