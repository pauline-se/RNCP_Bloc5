from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import requests  # to get image from the web
import shutil  # to save it locally
from PIL import Image
import ast
from tensorflow.keras import backend, layers
import ast
from tensorflow.keras import backend, layers
import os

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'kjqè73JJhsjhvahel'



class FixedDropout(layers.Dropout):
    def _get_noise_shape(self, inputs):
        if self.noise_shape is None:
            return self.noise_shape
        symbolic_shape = backend.shape(inputs)
        noise_shape = [symbolic_shape[axis] if shape is None else shape
                       for axis, shape in enumerate(self.noise_shape)]
        return tuple(noise_shape)


model = load_model('model.h5',
                   custom_objects={'FixedDropout': FixedDropout(rate=0.4)})

model.make_predict_function()
# reading the data from the file
with open('dictionnaire.txt') as f:
    data = f.read()
# reconstructing the data as a dictionary
d = ast.literal_eval(data)

#TO DO 
#Try to fill the predict_label function , where we will load image , transform it to an array , reshape it and predict the class of the image
def predict_label(img_path):
    i = image.load_img(img_path, target_size=(240,240))#add image.load_img method and take as argument the image path and the target image size (240,240)
    i = image.img_to_array(i)#transform the image to an array of pixels
    i = np.reshape(i, (1, 240, 240, 3))# reshape the image to (1, 240, 240, 3) size
    p = model.predict(i)
    in_max = np.where(p[0] == np.max(p))
    return d[in_max[0][0]]

# routes


@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")


@app.route("/about")
def about_page():
    return "CNN Car Classification"


@app.route('/link', methods=('GET', 'POST'))
def link():
    if request.method == 'POST':
        if request.form['action'] == 'Upload Image':
            img = request.files['my_image']
            img_path = "static/" + img.filename
            img.save(img_path)
            a = img.filename
            m = predict_label(img_path)
            return render_template("index.html", prediction=m, a=a)
        link = request.form['link']
        filename = link.split("/")[-1]
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open("static/" + filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image sucessfully Downloaded: ', filename)
            img_path = "static/" + filename
            a = filename
            m = predict_label(img_path)
            return render_template("index.html", prediction=m, a=a)


if __name__ == '__main__':
    #app.debug = True
    app.run(debug=True, host='0.0.0.0')
