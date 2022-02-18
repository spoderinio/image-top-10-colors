import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


img = Image.open(
    "/mnt/m2-storage/Python projects/Image-Colour-Palette-Generator/static/raccoon.jpg")


def get_colors(img):
    img_array = np.asarray(img)
    clt = KMeans(n_clusters=10)
    clt.fit(img_array.reshape(-1, 3))
    top10 = clt.cluster_centers_
    print(top10)
    top10_list = top10.tolist()

    hex_list = []
    for i in range(len(top10_list)):

        col = rgb2hex(int(top10_list[i][0]), int(
            top10_list[i][1]), int(top10_list[i][2]))
        hex_list.append(col)
    print(hex_list)


app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
