import os
import secrets
from PIL import Image
from logging import debug
from flask import request,render_template,url_for,redirect,request,abort,Response
from sollutionChallenge import app
from sollutionChallenge import socketio

from sollutionChallenge.utils import access_camera
import numpy as np
import pandas as pd
from io import StringIO, BytesIO
import imutils
import cv2
import base64
from flask_socketio import SocketIO
from yaml import emit, emitter
from sollutionChallenge.utils.ObjectDetectorOptions import *
from sollutionChallenge.utils.access_camera import *

detector = load_model()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',title="SollutionChallenge",home="active")

@app.route('/contactus')
def contact():
    return render_template("contactus.html",title="Team")



@app.route('/ourmission')
def ourmission():
    return render_template("OurMission.html",title="mission")



@app.route('/meetourteam')
def meetourteam():
    return render_template("MeetOurTeam.html",title="MOT")

@app.route('/inference')
def inference():
    return render_template('RealTimeInference.html')

@app.route('/videofeed')
def videofeed():
    return Response(access_camera.gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

    
@socketio.on('image')
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # Process the image frame
    frame = imutils.resize(frame, width=700)
    # frame = cv2.flip(frame, 1)
    image = cv2.resize(frame, (512, 512))
    image_np = np.asarray(image)
    detections = detector.detect(image_np)
    image_np = visualize(image_np, detections)
    imgencode = cv2.imencode('.jpg', image_np)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    try:
        emit('response_back', stringData)
    except emitter.EmitterError:
        print('failed')
