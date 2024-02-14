from flask import Flask, flash, render_template, request, redirect, url_for
import urllib.request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wtforms.validators import InputRequired
from keras.models import load_model
from keras.preprocessing import image
from PIL import Image


# name = predictions

plt.title('roses.jpg')

# image = img.imread('roses.jpg')
# plt.imshow(image)
# plt.show()
# img = Image.open("C:\Users\91955\Downloads\roses.jpg")

# Display the image
# img.show()  

app = Flask(__name__)


dic = {0: 'daisy', 1: 'dandelion', 2: 'roses', 3 : 'sunflowers', 4 : 'tulip'}

model = load_model('my_best_flower.h5')

def pred_label(img_path, threshold=0.9):
    img = Image.open(img_path)
    img = img.resize((150, 150))
    img_array = np.array(img) 
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add an extra dimension
    prediction = model.predict(img_array)
    print("Raw Predictions:", prediction)
    predicted_class_index = np.argmax(prediction)

    if prediction[0][predicted_class_index] > threshold:
        return "daisy"

    if prediction[1][predicted_class_index] > threshold:
        return "dandelion"

    if prediction[2][predicted_class_index] > threshold:
        return "roses"

    if prediction[3][predicted_class_index] > threshold:
        return "sunflowers"

    
    else:
        return "tulip"





app.config['SECRET_KEY'] = 'supersecreatkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']


# def allowed_file(filename):
#         photos= UploadSet('photos', ('png', 'jpg'))

class uploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

 



@app.route("/", methods=['GET', 'POST'])
# @app.route("/home", methods=['GET', 'POST'])
def index():
    form = uploadFileForm()
    result = None
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        

        
        # return "File Has Been Uploaded."
        result = pred_label(filepath)
    return render_template('index.html',  form=form, result=result)



    
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static/', filename='files' + filename), code=301)
 

def get_output():
     if request.method == 'POST':
         img = request.files['my_image']
         image_path = "static/files" + img.filename
         img.save(image_path)
         p = pred_label(image_path)
     return render_template('index.html', predicted_class = p, image_path = image_path ) 


if __name__=='__main__':
    app.run(debug=True)