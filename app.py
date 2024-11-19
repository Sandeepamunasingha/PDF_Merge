import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from PyPDF2 import PdfMerger

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/merge')
def merge_page():
    return render_template('merge.html')

@app.route('/combine', methods=['POST'])
def combine_pdfs():
    files = request.files.getlist('pdf_files')
    merger = PdfMerger()
    
    for file in files:
        if file.filename.endswith('.pdf'):
            merger.append(file)
    
    output_path = os.path.join(UPLOAD_FOLDER, 'combined.pdf')
    merger.write(output_path)
    merger.close()

    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return "Error: The file could not be saved.", 500

if __name__ == '__main__':
    app.run(debug=True)
