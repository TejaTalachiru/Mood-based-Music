from flask import Flask,request
import os
import cv2
import numpy as np
from keras.preprocessing import image
import warnings
warnings.filterwarnings("ignore")
from keras.preprocessing.image import load_img, img_to_array 
from keras.models import  load_model
# import matplotlib.pyplot as plt
import numpy as np
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import threading
from typing import Union
import av
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})
app = Flask(__name__)
@app.route('/',methods=['POST'])
@cross_origin()
def getMood():
    face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    model = load_model("best_model.h5")
    img_stream = request.files['emoji'].read()
    np_img = np.frombuffer(img_stream, np.uint8)
    image = cv2.resize(cv2.imdecode(np_img, cv2.IMREAD_COLOR),
                       dsize=(224, 224), interpolation=cv2.INTER_CUBIC
                       )
    
    print(image.shape)
    i = image/255
    img_arr = np.array([i])
    predictions = model.predict(img_arr, verbose=False)
    max_index = np.argmax(predictions[0])
    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    predicted_emotion = emotions[max_index]
    return jsonify(predicted_emotion)

    # faces_detected = face_haar_cascade.detectMultiScale(img_arr, 1.32, 5)
    # if faces_detected:
    #     predictions = model.predict(img_arr, verbose=False)
    #     max_index = np.argmax(predictions[0])
    #     emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    #     predicted_emotion = emotions[max_index]
    #     return jsonify(predicted_emotion)
    # else:
    #     return jsonify("no")
    # while True:
    #     gray_img = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)

    #     faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

    #     for (x, y, w, h) in faces_detected:
    #         cv2.rectangle(img_arr, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
    #         roi_gray = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image
    #         roi_gray = cv2.resize(roi_gray, (224, 224))
    #         img_pixels = image.img_to_array(roi_gray)
    #         img_pixels = np.expand_dims(img_pixels, axis=0)
    #         img_pixels /= 255

    #         predictions = model.predict(img_pixels, verbose=False)

    #         # find max indexed array
    #         max_index = np.argmax(predictions[0])

    #         emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    #         predicted_emotion = emotions[max_index]
    #         return jsonify(predicted_emotion)
    #     return jsonify("no")


if __name__ == "__main__":
    app.run(debug=True)


# load model
