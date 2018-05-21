import os
'''
os.chdir('weights/')
os.system('rm yolov2-tiny.weights')
os.system('wget https://pjreddie.com/media/files/yolov2-tiny.weights')
os.chdir('../')      
'''
from flask import Flask, render_template, Response, request, send_file
import time
# import bg_removal as brm
import label as lb
import rawpy
import imageio

app = Flask(__name__,static_folder='images')

# _,frame = cap.read()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html",good='',bad='')

@app.route("/upload", methods=['POST'])
def upload():
    try:
        t0 = time.clock()
        target = os.path.join(APP_ROOT, 'images/')
        # print(target)

        if not os.path.isdir(target):
            os.mkdir(target)
        destination = ''
        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
        if '.nef' in destination.lower():
           with rawpy.imread(destination) as raw:
              rgb = raw.postprocess()
           destination = destination.split('.')[0]+'.jpg'
           imageio.imwrite(destination, rgb)
        # brm.segment(destination)
        result = lb.main(destination)
        os.system('rm '+destination)
        
        return render_template("upload.html",good='Good '+str(result['good']),bad='Bad '+str(result['bad']))
    except:
        return render_template("upload.html",good='',bad='')
        
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("upload.html",good='',bad='')

if __name__ == "__main__":
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port, debug=True)


