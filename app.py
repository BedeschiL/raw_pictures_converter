import zipfile
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import os
import uuid
from flask import send_file

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['CONVERTED_FOLDER'] = 'static/converted/'
app.config['ALLOWED_EXTENSIONS'] = {'nef', 'cr2', 'arw', 'dng', 'raw', 'orf'}
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 50MB max

# Créer les dossiers s'ils n'existent pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def convert_to_png(input_path, output_path):
    try:
        # Vérifier l'extension pour les fichiers ORF
        if input_path.lower().endswith('.orf'):
            import rawpy
            import imageio

            with rawpy.imread(input_path) as raw:
                rgb = raw.postprocess()
                imageio.imsave(output_path, rgb)
        else:
            # Traitement normal pour les autres formats
            with Image.open(input_path) as img:
                img.save(output_path, 'PNG')
        return True
    except Exception as e:
        print(f"Erreur de conversion: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('files')
    results = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            raw_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
            png_filename = f"{os.path.splitext(filename)[0]}.png"
            png_path = os.path.join(app.config['CONVERTED_FOLDER'], f"{unique_id}_{png_filename}")

            file.save(raw_path)
            success = convert_to_png(raw_path, png_path)

            results.append({
                'original': filename,
                'converted': f"{unique_id}_{png_filename}" if success else None,
                'success': success
            })

    return {'results': results}


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['CONVERTED_FOLDER'], filename)
@app.route('/download_all', methods=['POST'])
def download_all():
    try:
        data = request.get_json()
        if not data or 'files' not in data:
            return {'error': 'Invalid request'}, 400

        # Création d'un ZIP en mémoire
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename in data['files']:
                file_path = os.path.join(app.config['CONVERTED_FOLDER'], filename)
                if os.path.exists(file_path):
                    zf.write(file_path, os.path.basename(file_path))

        memory_file.seek(0)
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name='converted_images.zip'
        )
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)