from flask import Flask, render_template, request,send_from_directory,send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
# All pw
app = Flask(__name__)

	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      #f.save(secure_filename(f.filename))
      return send_file(f.filename,as_attachment=True)#send_from_directory("",f.filename)
		
if __name__ == '__main__':
   app.run(debug = True,port=5500)