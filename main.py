import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from flask import Flask, render_template, redirect, url_for


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


img = Image.open(
    "/mnt/m2-storage/Python projects/Image-Colour-Palette-Generator/static/raccoon.jpg")

hex_list = []


def get_colors(img):
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


app = Flask(__name__)


@app.route('/')
def home():
    get_colors(img)
    return render_template("index.html", hex_list=hex_list)


if __name__ == "__main__":
    app.run(debug=True)
