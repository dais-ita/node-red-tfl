import json, argparse, time

from flask import Flask, request, Response
from flask_cors import CORS

import os

import numpy as np
import urllib
import cv2

import base64
from PIL import Image
from StringIO import StringIO


def readb64(base64_string):
    sbuf = StringIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

def encIMG64(image):
    retval, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer)



def URLtoImage(url):
    response = urllib.urlopen(url)
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
    return image


def generate_frames(video,frame_step,loop=False):
    frame_count = -1
    while(1):
        ret, frame = video.read()
        frame_count += 1
        if not frame is None:
            if frame_count == 0 or (frame_count +1) % frame_step == 0:
                jpg_as_text = encIMG64(frame)
                print("yielding frame: " +str(frame_count+1))
                yield jpg_as_text
            else:
                continue
        else:
            break
    yield "fin"
    return

    


app = Flask(__name__)
cors = CORS(app)
@app.route("/stream-video", methods=['POST'])
def StreamVideo():
    if 'camera_id' in request.form.keys():
        camera_id = request.form["camera_id"]

        api_url = "http://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/00001.{}.mp4"
        request_url = api_url.format(str(camera_id))

        
        video = cv2.VideoCapture(request_url)

    

    return Response(generate_frames(video,50), mimetype='application/text')


@app.route("/stream-video/id/<string:camera_id>", methods=['GET'])
def StreamVideoFromId(camera_id):
    api_url = "http://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/00001.{}.mp4"
    request_url = api_url.format(str(camera_id))

    
    video = cv2.VideoCapture(request_url)

    

    return Response(generate_frames(video,50), mimetype='application/text')



# @app.route("/car-detector/image", methods=['POST', 'GET'])
# def GetRatingFromImage():
#     if request.method == 'POST':
#         if 'image' in request.files:
#             input_image = cv2.imdecode(numpy.fromstring(request.files['image'].read(), numpy.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)

#             result = dais_detctor.DetectInImage(input_image)

#             json_data = json.dumps({'cars': [{"pixel_coords":car_result[0].tolist(),"confidence":float(car_result[1])} for car_result in result["car"]]})
            
#             return json_data

#         if 'image' in request.form.keys():
#             input_image = readb64(request.form["image"])

            
#             result = dais_detctor.DetectInImage(input_image)

#             json_data = json.dumps({'cars': [{"pixel_coords":car_result[0].tolist(),"confidence":float(car_result[1])} for car_result in result["car"]]})
            
#             return json_data


#         return 'error'
#     return '''
#     <!doctype html>
#     <title>Upload Image File to Detect Cars</title>
#     <h1>Upload Image File to Detect Cars</h1>
#     <form method=post enctype=multipart/form-data>
#     <p><input type=file name=image>
#     <input type=submit value=Upload>
#     </form>
#     '''


if __name__ == "__main__":
    print('Starting the API')
    app.run(host='0.0.0.0', port=5030)