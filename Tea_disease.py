





from flask import Flask, render_template
from flask import request
from flask import redirect, url_for
from flask.wrappers import Request
import os


app=Flask(__name__)



BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')
MODEL_PATH = os.path.join(BASE_PATH,'static/models/')

model_sgd_path = os.path.join(MODEL_PATH,'Tea_leaf.h5')

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
            results = pipeline_model(path_save,scaler,model_sgd)
            hei = getheight(path_save)
            print(results)
            return render_template('upload.html',fileupload=True,extension=False,data=results,image_filename=filename,height=hei)



            
        else:
            print('Use only the extension with .jpg, .png, .jpeg')

            return render_template('upload.html',extension=True,fileupload=False)
    else:
        return render_template('upload.html',fileupload=False,extension=False)



if __name__ == "__main__":
    app.run(debug=True)