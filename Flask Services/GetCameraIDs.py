#https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/

from flask import Flask, request
from flask_cors import CORS

import json

import urllib.request
import xmltodict
import xml.etree.ElementTree as ET


app = Flask(__name__)
cors = CORS(app)
@app.route("/tfl-api/camera-ids", methods=['GET'])
def GetCameraId():

    api_url = 'https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/'

    speed_limits = urllib.request.urlretrieve(api_url)

    tree = ET.parse(speed_limits[0])
    
    root = tree.getroot()

    contents = root.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Contents')
    
    camera_ids = []

    for content in contents:
        key = content.find('{http://s3.amazonaws.com/doc/2006-03-01/}Key').text
        if(key[-3:] == "jpg"):
            camera_ids.append(key.replace("00001.","").replace(".jpg",""))

    camera_dict = {"camera_ids": camera_ids}
    
    #return str(camera_ids)
    return json.dumps(camera_dict)


if __name__ == "__main__":
    #print(GetCameraId())

    print('Starting the API')
    app.run(host='0.0.0.0',port=5002)