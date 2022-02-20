import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import os
from colorthief import ColorThief


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


hex_list = []

# it works damn slow, so I used ColorTheaf instead


def get_colors_kmeans(img):
    hex_list.clear()
    img_array = np.asarray(img)
    clt = KMeans(n_clusters=10)
    clt.fit(img_array.reshape(-1, 3))
    top10 = clt.cluster_centers_
    print(top10)
    top10_list = top10.tolist()

    for i in range(len(top10_list)):

        col = rgb2hex(int(top10_list[i][0]), int(
            top10_list[i][1]), int(top10_list[i][2]))
        hex_list.append(col)
        print(hex_list)
    return hex_list


def get_colors(img):
    hex_list.clear()
    color_thief = ColorThief(img)
    top10_list = color_thief.get_palette(color_count=11)
    for i in range(len(top10_list)):

        col = rgb2hex(int(top10_list[i][0]), int(
            top10_list[i][1]), int(top10_list[i][2]))
        hex_list.append(col)
        print(hex_list)
    return hex_list


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/mnt/m2-storage/Python projects/Image-Colour-Palette-Generator/static/images"


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST", "GET"])
def result():
    file = request.files['file']
    print(file.filename)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    full_image_path = f"static/images/{file.filename}"
    get_colors(full_image_path)
    return render_template("index.html", image=full_image_path, hex_list=hex_list)


if __name__ == "__main__":
    app.run(debug=True)
