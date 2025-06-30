#Image Color Palette Site
from collections import Counter

import numpy as np
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
from PIL import Image


import os
from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def color_delta(color1, color2):
    return np.sqrt(np.sum((np.array(color1) - np.array(color2)) ** 2))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/',methods=['GET','POST'])
def home():
    image_url =None
    lst = list()
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '' and allowed_file(image.filename):
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(image_path)
                image_url = f"/static/uploads/{image.filename}"


                # Image data collection
                my_img = Image.open(image_path).convert('RGB')
                img_array = np.array(my_img)

                pixels = img_array.reshape(-1,3)

                # rounded_pixels = (pixels[:, :3] // 10) * 10


                #KMEANS CLUSTERING
                kmeans = KMeans(n_clusters=10,random_state=42).fit(pixels)

                #center of clusters
                centers = kmeans.cluster_centers_.astype(int)

                labels = kmeans.labels_
                label_counts = Counter(labels)


                # uniquecols,counts = np.unique(pixels,axis=0,return_counts=True)
                # color_counts = sorted(zip(uniquecols, counts), key=lambda x: -x[1])
                color_counts = sorted([(tuple(centers[i]), label_counts[i]) for i in range(len(centers))],
                                      key=lambda x: -x[1])
                delta = [color_delta(centers[0], center) for center in centers]

                for color, count in color_counts:
                    # if color[3] != 0:  # exclude fully transparent pixels
                    # clean_color = tuple(int(c) for c in color[:3])  # exclude alpha
                    # lst.append(clean_color)
                    rgb_color = tuple(map(int, color))  # This converts np.int64 to int
                    hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_color)
                    lst.append({
                        'rgb': rgb_color,
                        'hex': hex_color,
                        'count': count
                    })


                    if len(lst) >= 10:
                        break

    return render_template(template_name_or_list='template_index.html',image_url=image_url,color_list=lst)






if __name__ == "__main__":
    app.run(debug=True,port=5000)







    # for i in os_fspath('/static/uploads'):
    #     os.remove(i)





# my_img = Image.open('C:/Users/HP/Downloads/nnn.png')
#
# img_array = np.array(my_img)
#
# pixels = img_array.reshape(-1,4)
# uniquecols,counts = np.unique(pixels,axis=0,return_counts=True)
#
# color_counts = list(zip([tuple(color) for color in uniquecols],counts))
# lst=list()
# for color, count in sorted(zip(uniquecols, counts), key=lambda x: -x[1])[:10]:
#     clean_color = tuple(int(c) for c in color)
#     lst.append(clean_color)
#     print(f"Color: {clean_color}, Count: {count}")
#
#
