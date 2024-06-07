from flask import Flask, request, jsonify
from ultralytics import YOLO
import numpy as np
import os
from PIL import Image

app = Flask(__name__)

model = YOLO('C:/Users/Josh/Desktop/WebDev/Python/imageIdentifiers/runs2/classify/train/weights/last.pt')  # load a custom model

# POST REQUEST PREDICTION CODE
@app.route('/identify', methods=['POST'])
def identify_image():
    if request.method == 'POST':
        # Get the image file from the request
        image_file = request.files['image']

        # Save the image temporarily
        temp_image_path = 'temp.jpg'
        image = Image.open(image_file)
        image.save(temp_image_path)

        try:
            # Predict on the image
            results = model(temp_image_path)

            # Get the names and probabilities
            names_dict = results[0].names
            probs = results[0].probs.data.tolist()

            # Get the identification
            identification = names_dict[np.argmax(probs)]
            print(identification) #print to console

            # Delete the temporary image file
            os.remove(temp_image_path)

            # Return the identification as JSON response
            return jsonify({'identification': identification}), 200
        except Exception as e:
            # Handle any errors and return an error response
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Method Not Allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)