import numpy as np
import requests  # to get image from the web
import shutil  # to save it locally
import ast
import ast
import random as rd
import os
from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras import backend, layers
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from urllib.parse import urlparse


app = Flask(__name__, template_folder='templates')

# Import configuration from config.py
app.config.from_pyfile('config.py')


class FixedDropout(layers.Dropout):
    def _get_noise_shape(self, inputs):
        if self.noise_shape is None:
            return self.noise_shape
        symbolic_shape = backend.shape(inputs)
        noise_shape = [symbolic_shape[axis] if shape is None else shape for axis,
                       shape in enumerate(self.noise_shape)]
        return tuple(noise_shape)

model = load_model("model.h5", custom_objects={"FixedDropout": FixedDropout(rate=0.4)})

model.make_predict_function()

# reading the data from the file


with open('dictionary.txt') as f:
    data = f.read()

# reconstructing the data as a dictionary
dictionary = ast.literal_eval(data)



#########################
###     FUNCTIONS     ###
#########################

def predict_label(img_path):
    i = image.load_img(img_path, target_size=(240, 240))
    i = image.img_to_array(i)/255.0
    i = i.reshape(1, 240, 240, 3)
    p = model.predict(i)

    predicted_class_index = np.argmax(p)
    confidence_cal = p[0][predicted_class_index]
    predicted_class = dictionary[predicted_class_index]

    # If confidence < 95%, special value
    if confidence_cal < 0.95:
        return -1, "low_confidence", confidence_cal

    return predicted_class_index, predicted_class, confidence_cal


def get_emoji(predicted_class_index):
    emoji_mapping = {
        0: "🐝",
        1: "🦋",
        2: "🐞"
    }
    emoji = emoji_mapping.get(predicted_class_index, "")
    return emoji

app.jinja_env.globals.update(get_emoji=get_emoji)

def get_random_anecdotes(predicted_class_index):
    with open(f'static/anecdotes/{predicted_class_index}.txt', 'r', encoding='utf-8') as f:
        anecdotes = f.readlines()
    random_anecdotes = rd.sample(anecdotes, 3)
    return random_anecdotes

app.jinja_env.globals.update(get_random_anecdotes=get_random_anecdotes)




#########################
###      ROUTES       ###
#########################

@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return app.send_static_file(filename)

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/predictions.html")
def predictions():
    return render_template("predictions.html")

@app.route("/gestion.html")
def gestion():
    return render_template("gestion.html")

@app.route("/linkimg", methods = ("GET", "POST"))
def linkimg():
    error = None
    if request.method == "POST":

        # IMAGE parameters
        if request.form["action"] == "Envoyer image":
            img = request.files['my_image']

            # Check if no file was selected
            if not img:
                error = "Vous n'avez pas sélectionné d'image"
            else:
                # Check if the file is an image
                try:
                    Image.open(BytesIO(img.read()))
                    img.seek(0)  # Rewind the file to play it again
                except UnidentifiedImageError:
                    error = "Le fichier sélectionné n'est pas une image !"
                else:
                    os.makedirs("static/user_content", exist_ok=True)
                    img_path = "static/user_content/" + img.filename
                    img.save(img_path)
                    a = img.filename
                    predicted_class_index, m, confidence = predict_label(img_path)
                    if confidence < 0.96:
                        color="Red"
                        affichage_niveau="Faible"
                        width="30%"
                    elif (confidence >= 0.96) and (confidence < 0.98):
                        color="Orange"
                        affichage_niveau="Modéré"
                        width="60%"  
                    elif confidence >= 0.98:
                        color="Green"
                        affichage_niveau="Elevé"
                        width="90%"                                           
                    confidence = "{:.3f} %".format(confidence * 100)
                    section_id = "section_prediction"
                    return render_template("predictions.html"
                                           , prediction=m
                                           , confidence=confidence
                                           , a=a, color=color
                                           , affichage_niveau=affichage_niveau
                                           , width=width
                                           , predicted_class_index=predicted_class_index
                                           , section_id=section_id)

    return render_template("predictions.html", error=error)


@app.route('/linkurl', methods=('GET', 'POST'))
def linkurl():
    error = None
    if request.method == 'POST':
        # URL parameters
        link_url = request.form['linkurl']

        # Check if the link field is empty
        if not link_url:
            error = "Vous n'avez pas inséré d'URL !"
        else:
            parsed_url = urlparse(link_url)
            filename = os.path.basename(parsed_url.path)  # Use only URL path for the file name
            r = requests.get(link_url, stream=True)

            # Check if the content is an image
            if 'image' in r.headers['Content-Type']:

                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True

                    # Create the directory if it doesn't exist
                    os.makedirs("static/user_content", exist_ok=True)

                    # Open a local file with wb ( write binary ) permission.
                    with open("static/user_content/" + filename, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)

                    print('Image téléchargée avec succès: ', filename)
                    img_path = "static/user_content/" + filename
                    a = filename
                    predicted_class_index, m, confidence = predict_label(img_path)
                    if confidence < 0.96:
                        color="Red"
                        affichage_niveau="Faible"
                        width="30%"
                    elif (confidence >= 0.96) and (confidence < 0.98):
                        color="Orange"
                        affichage_niveau="Modéré"
                        width="60%"  
                    elif confidence >= 0.98:
                        color="Green"
                        affichage_niveau="Elevé"
                        width="90%"                                           
                    confidence = "{:.3f} %".format(confidence * 100)
                    section_id = "section_prediction"
                    return render_template("predictions.html", prediction=m, confidence=confidence, a=a, color=color, affichage_niveau=affichage_niveau, width=width, predicted_class_index=predicted_class_index, section_id=section_id)
                else:
                    error = "L'URL ne doit pas rediriger vers une image."
            else:
                error = "L'URL ne doit pas rediriger vers une image."

    return render_template("predictions.html", error=error)




#########################
###        RUN        ###
#########################

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="2024")