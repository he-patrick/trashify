from keras.models import model_from_json
import cv2
from PIL import Image
import numpy as np

# load the model from the json file
json_file = open('backend/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("backend/model.h5")

# predicting on a single image
def convert_to_array(img):
    im = cv2.imread(img)
    img = Image.fromarray(im, 'RGB')
    image = img.resize((100, 100))
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
    ar = convert_to_array(file)
    ar = ar/255
    label = 1
    a = []
    a.append(ar)
    a = np.array(a)
    score = loaded_model.predict(a, verbose=1)
    acc = np.max(score)
    
    if acc < 0.6:
        label_index = -1
    else:
        label_index = np.argmax(score)
    
    trash = get_trash_type(label_index)
    print("The predicted trash is a "+trash+" with accuracy = "+str(acc))

predict_trash("backend/trash10.jpg")