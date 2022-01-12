import numpy as np
import tensorflow as tf


#from tensorflow import InteractiveSession

config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5
config.gpu_options.allow_growth = True
session = tf.compat.v1.InteractiveSession(config=config)

from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


from flask import Flask, render_template
from flask import request
from flask import redirect, url_for
#from flask.wrappers import Request
import os


app=Flask(__name__)



BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')
#MODEL_PATH = os.path.join(BASE_PATH,'static/models/')

model = load_model('static/models/Tea_leaf.h5')


def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(256, 256))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="healthy_tea"
        print(preds)
    elif preds==1:
        preds="Gray_blight"
    else:
        preds="Healthy tea leaf"
    
    return preds





@app.errorhandler(404)
def error404(error):
    message = "ERROR 404 OCCURRED. Page Not Found. Please go the home page and try again"
    return render_template("error.html",message=message) # page not found

@app.errorhandler(405)
def error405(error):
    message = 'Error 405, Method Not Found'
    return render_template("error.html",message=message)

@app.errorhandler(500)
def error500(error):
    message='INTERNAL ERROR 500, Error occurs in the program'
    return render_template("error.html",message=message)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method=="POST":
        upload_file = request.files['image_name']
        filename=  upload_file.filename
        print('The filename that has been uploaded=', filename)

#filename
        ext= filename.split('.')[-1]
        print('The extension of the filename is',ext)
        if ext.lower() in ['png', 'jpg', 'jpeg']:
            path_save = os.path.join(UPLOAD_PATH,filename)
            upload_file.save(path_save)
            print('File saved sucessfully')
            # send to pipeline model
            preds = model_predict(path_save, model)
            result=preds
            return result
            
        else:
            print('Use only the extension with .jpg, .png, .jpeg')

            return render_template('upload.html')
    else:
            return render_template('upload.html')



if __name__ == "__main__":
    app.run(debug=True)