#POST REQUEST TEST CODE

import requests

url = 'http://localhost:5000/identify'
files = {'image': open('test_image1.jpg', 'rb')}
response = requests.post(url, files=files)

print(response.json())