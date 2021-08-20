from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
from com_in_ineuron_ai_utils.utils import decodeImage
from predict import ricegrains
from countwheatgrains import  count
from PIL import Image

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)




#@cross_origin()
class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = ricegrains(self.filename)



@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index5.html')


PEOPLE_FOLDER = os.path.join('/home/knoldus/Downloads/rice-quality-analysis-master (1)/Rice-Grain-Image-Classification-master/static')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
@app.route("/predictRoute", methods=['POST'])
@cross_origin()
def predictRoute():
    if request.method=='POST':
        #image = request.json['filename']
        file = request.files['filename']
        # Read the image via file.stream
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'inputImage.jpg'))
        image = Image.open(file.stream)

        #decodeImage(image, clApp.filename)
        try:
            result = clApp.classifier.predictionricegrains()
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'inputImage.jpg')
            cnt = count()
            print(cnt)
            print(type(result), len(result))
            predict = result[0]['image']
            cnt = result[1]
            result=result[2]


        except:
           return render_template('index5.html',predict="Low Probabiliyt Score",cnt="No Count",user_image = "Image is not Available",result="No Result")


    return render_template('index5.html', predict=predict, cnt=cnt, user_image=full_filename,result=result)



#port = int(os.getenv("PORT"))
if __name__ == "__main__":
    clApp = ClientApp()
    #app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', port=8000, debug=True)
