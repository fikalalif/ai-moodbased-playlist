# from flask import Flask, request, redirect, session, render_template,url_for
# from emotion_model import detect_emotion_from_webcam
# from sentiment_model import detect_sentiment
# from spotify_helper import get_playlist
# from spotipy.oauth2 import SpotifyOAuth
# import spotipy
# from flask import session
# from dotenv import load_dotenv
# load_dotenv()
# import base64
# from PIL import Image
# from io import BytesIO
# import os


# app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET_KEY", "my_super_secret_dev_key")

# sp_oauth = SpotifyOAuth(
#     scope='playlist-read-private'
# )

# @app.route('/callback')
# def callback():
#     code = request.args.get('code')
#     token_info = sp_oauth.get_access_token(code)
#     access_token = token_info['access_token']
    
#     # Simpan token ke session
#     session['access_token'] = access_token

#     return redirect(url_for('index'))


# @app.route("/", methods=["GET", "POST"])
# def index():
#     mood = None
#     playlist_url = None

#     access_token = session.get('access_token')
#     if not access_token:
#         return redirect(sp_oauth.get_authorize_url())

#     sp = spotipy.Spotify(auth=access_token)

#     if request.method == "POST":
#         if 'use_webcam' in request.form:
#             mood = detect_emotion_from_webcam()
#         else:
#             text = request.form['user_text']
#             mood = detect_sentiment(text)

#     mood = detect_emotion_from_webcam()

#     if mood is None:
#         return "Gagal mendeteksi emosi. Pastikan wajah terlihat jelas di kamera."

#     if  mood not in MOOD_TO_GENRE:
#         return f"Emosi '{mood}' tidak dikenali. Hasil: {mood}"

#         playlist_url = get_playlist(mood, sp)
#         if playlist_url is None:
#             return "Gagal mendapatkan playlist untuk mood: " + mood

#     return render_template("index.html", mood=mood, playlist_url=playlist_url)



# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, session
from spotify_helper import get_playlist, create_spotify_client
from sentiment_model import detect_sentiment
from emotion_model import detect_emotion_from_webcam
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
