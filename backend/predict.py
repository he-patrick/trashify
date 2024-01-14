from keras.models import model_from_json
import cv2
from PIL import Image
import numpy as np
from flask_cors import CORS
from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000"])

@app.route('/')
def start():
    return ""


@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # # Extract the base64 image data from the request
        # image_data = request.data.decode('utf-8')

        # # The data URL contains a header and the base64 data separated by a comma.
        # # We only need the base64 data.
        # header, base64_data = image_data.split(',', 1)

        # # Decode the base64 string
        # image_bytes = base64.b64decode(base64_data)



        # # Save the image to a file or further process it as needed
        # with open('captured_image.jpeg', 'wb') as image_file:
        #     image_file.write(image_bytes)


        image_file = request.files['image']
        print(image_file)
        # Ensure the image is saved or processed correctly
        result = predict_trash(image_file)
        print(result)
        return jsonify({'result': result})
   
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)

# load the model from the json file
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")

# predicting on a single image
def convert_to_array(img):
    im = Image.open(img).convert("RGB")    
    im.save('backend' + img[:-4] + '.jpg', quality=95, optimize=True)
    im2 = cv2.imread(im)
    im2 = Image.fromarray(im2, 'RGB')
    image = im2.resize((100, 100))
    return np.array(image)
def get_trash_type(label):
    if label == 0 or label == 1:
        return "paper trash"
    elif label == 2 or label == 3:
        return "aluminum trash"
    elif label == 4 or label == 5:
        return "plastic trash"
    else:
        return "other trash"
def predict_trash(file):
    print("Predicting .................................")
    return "plastic"
    ar = convert_to_array(file)
    print(ar)
    ar = ar/255
    label = 1
    a = []
    a.append(ar)
    a = np.array(a)
    score = loaded_model.predict(a, verbose=1)
    print(score)
    acc = np.max(score)
    
    if acc < 0.6:
        label_index = -1
    else:
        label_index = np.argmax(score)
    
    trash = get_trash_type(label_index)
    print("The predicted trash is a "+trash+" with accuracy = "+str(acc))
    return trash