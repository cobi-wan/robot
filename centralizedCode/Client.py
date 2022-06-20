from __future__ import print_function
import requests
import json
import cv2
from MapData import mapping
from Classes import environment
import time

addr = 'http://localhost:5000'
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

# tS = time.monotonic_ns()
# while True:
#     if time.monotonic_ns() - tS > 1000000 * env.timeStep:
env = mapping()
img = env.UIwBots
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
# decode response
print(json.loads(response.text))
        # tS = time.monotonic_ns()

# expected output: {u'message': u'image received. size=124x124'}
