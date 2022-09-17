from flask import Flask, render_template, request, send_file

from transcribe import generate_mom

app = Flask(__name__)
global f

@app.route('/')
def upload_file():
   return render_template('upload.html')

@app.route('/generate', methods = ['GET', 'POST'])
def generate():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename) 
        path = generate_mom(f.filename)
        with open(path, 'r') as f:
            t=f.read() 
        return render_template('upload.html', t=t)

@app.route('/download')
def download_file():
    path = 'your_mom.txt'
    return send_file(path, as_attachment=True)
