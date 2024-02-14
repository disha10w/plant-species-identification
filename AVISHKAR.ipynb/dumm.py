from flask import Flask, flash, render_template, request, redirect, url_for
import urllib.request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from keras.models import load_model
from keras.preprocessing import image


app = Flask(__name__)

dic={ 0: "Normal Eye", 1:"Fluid Eye"}

model= load_model(r'C:\Users\prach\Downloads\Yogi Project+ main\Yogi Project (1)\Yogi Project\Yogi Project\eye-100.h5')

#model.make_prediction_function()

def predict_label(img_path):
    i= image.load_img(img_path, target_size=(150,150))
    i= image.img_to_array(i)/255.0
    i= i.reshape.predict_classes(i)
    return dic[p[0]]


app.config['SECRET_KEY'] = 'supersecreatkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']


def allowed_file(filename):
        photos= UploadSet('photos', ('png', 'jpg'))

class uploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

   



@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def index():
    form = uploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return "File Has Been Uploaded."


    return render_template('index.html', form=form)

@app.route("/upload", methods = ['GET', 'POST'])
# def upload_image():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         #print('upload_image filename: ' + filename)
#         flash('Image successfully uploaded and displayed below')
#         return render_template('index.html', filename=filename)
#     else:
#         flash('Allowed image types are - png, jpg, jpeg, gif')
#         return redirect(request.url)
    
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='files/' + filename), code=301)
 

def get_output():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/files" + img.filename
        img.save(img_path)
        p = predict_label(img_path)
    return render_template('index.html', prediction = p, img_path = img_path) 


if __name__=='__main__':
    app.run(debug=True)