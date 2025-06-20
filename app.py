from flask import Flask, render_template, request, redirect, session
from spotify_helper import get_playlist, create_spotify_client
from sentiment_model import detect_sentiment
from dotenv import load_dotenv
import os
from flask import jsonify
import base64
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from fer import FER


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

sp = create_spotify_client()


@app.route('/', methods=['GET', 'POST'])
def index():
    mood = request.args.get('mood', None)
    playlist_url = None

    if request.method == 'POST':
        if 'text_input' in request.form and request.form['text_input']:
            mood = detect_sentiment(request.form['text_input'])

    if mood:
        playlist_url = get_playlist(mood, sp)

    return render_template('index.html', mood=mood, playlist_url=playlist_url)



@app.route('/detect_webcam_emotion', methods=['POST'])
def detect_webcam_emotion():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    image_data = base64.b64decode(data['image'].split(',')[1])
    image = Image.open(BytesIO(image_data)).convert('RGB')
    frame = np.array(image)

    detector = FER()
    result = detector.top_emotion(frame)

    if result:
        emotion, score = result
        return jsonify({'emotion': emotion})
    else:
        return jsonify({'emotion': 'neutral'})

if __name__ == '__main__':
    app.run(debug=True)