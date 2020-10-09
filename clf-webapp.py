import os
import tensorflow as tf
from flask import Flask,request,redirect,url_for,flash
from werkzeug.utils import secure_filename
from flask import render_template
from keras.models import load_model
import sys,keras
import numpy as np
from PIL import Image

classes = ['猿','イノシシ','カラス']
num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = './uploaded_file'
ALLOWED_EXTENSIONS = set(['png','jpg','gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
graph = tf.get_default_graph()#マルチスレッドで推論を２度以上回すときに、tfがグラフを共有できないと、エラーが出る。

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/clf-webapp',methods=['GET','POST'])
def upload_file():
    predictionResult=False
    commentFromRobot = '予測したい画像をアップロードして下さい'
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file found')
            return redirect(request.url)

        file = request.files['file']

        if file.filename =='':
            flash('No file found')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    
            global graph
            with graph.as_default():

                model = load_model('./models/animal_cnn_aug_Sat Sep 26 19:53:27 2020.h')

                image = Image.open(filepath)
                image = image.convert('RGB')
                image = image.resize((image_size,image_size))
                data = np.asarray(image)
                _x = []
                _x.append(data)
                _x = np.array(_x) 
            
                result = model.predict([_x])[0]

                predicted = result.argmax()
                animal = classes[predicted]

            predictionResult = True

            commentFromRobot = '{} は{}だと思われます。'.format(file.filename,animal)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            
    return render_template('clf-webapp.html',predictionResult=predictionResult,commentFromRobot = commentFromRobot)

from flask import send_from_directory
@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)    

@app.route('/test',methods=['GET','POST'])
def return_test_page():
    if request.method == 'POST':
        testFile1 = request.form['testFile1']
        testFile2 = request.form['testFile2']
        #return str(testFile1 + ':' + testFile2)
    
    return render_template('test_page.html')

if __name__=='__main__':
    app.run()

