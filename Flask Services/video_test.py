import numpy as np
import cv2

camera_id = "04500"

api_url = "http://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/00001.{}.mp4"
request_url = api_url.format(str(camera_id))

cap = cv2.VideoCapture(request_url)

while(cap.isOpened()):
    ret, frame = cap.read()

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()