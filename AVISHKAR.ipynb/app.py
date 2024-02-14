from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/form', methods=['POST'])
def predict():
    image_file = request.files['imagefile']
    image_path = "./static/files" + imagefile.filename
    imagefile.save(image_path)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000 , debug=True)

