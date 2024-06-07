from flask import Flask, request, redirect, url_for, send_file, render_template
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Crear directorios si no existen
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file_post():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('process_file', filename=file.filename))

@app.route('/process/<filename>', methods=['GET'])
def process_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file_path, sep='\t')

    processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename.replace('.tsv', '.xlsx'))
    df.to_excel(processed_file_path, index=False)

    return send_file(processed_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
