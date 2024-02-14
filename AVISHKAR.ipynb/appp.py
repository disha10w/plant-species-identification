from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from PIL import Image

app = Flask(__name__)

#dic = {0 : 'Normal Eye', 1 : 'Fluid Eye'}

#model = load_model('flue-test.h5')
#model.make_predict_function()

#def predict_label(img_path):
#	i = image.load_img(img_path, target_size=(100,100))
#	i = i.reshape(1, 100,100,3)
#	p = model.predict_class(i)
#	return dic[p[0]]



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
    


    # Return the predicted label
    #return predicted_label, binary_prediction
    
    
    


    


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")



@app.route("/", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/files" + img.filename	
		img.save(img_path)

		p = pred_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)