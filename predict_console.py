from flask import Flask, request, jsonify
from ultralytics import YOLO
import numpy as np
import os
from PIL import Image

app = Flask(__name__)

model = YOLO('C:/Users/Josh/Desktop/WebDev/Python/imageIdentifiers/runs/classify/train/weights/last.pt')  # load a custom model

#CONSOLE PREDICTION CODE
results = model('C:/Users/Josh/Desktop/WebDev/Python/imageIdentifiers/test_image1.jpg')  # predict on an image
names_dict = results[0].names
probs = results[0].probs.data.tolist()
print(names_dict)
print(probs)
print(names_dict[np.argmax(probs)])