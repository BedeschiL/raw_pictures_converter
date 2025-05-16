import zipfile
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from flask import send_file
from converters.raw_to_png import RawToPngConverter

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['CONVERTED_FOLDER'] = 'static/converted/'
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 50MB max

# Enregistrement des convertisseurs
CONVERTERS = {
    'raw_to_png': RawToPngConverter
}

# Créer les dossiers s'ils n'existent pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Vérifie si le fichier est supporté par un des convertisseurs"""
    if '.' not in filename:
        return False
        
    ext = filename.rsplit('.', 1)[1].lower()
    for converter in CONVERTERS.values():
        if ext in converter.supported_formats():
            return True
    return False

def get_converter(filename):
    """Retourne le convertisseur approprié pour le fichier"""
    ext = filename.rsplit('.', 1)[1].lower()
    for converter in CONVERTERS.values():
        if ext in converter.supported_formats():
            return converter
    return None

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
            
            # Trouver le bon convertisseur
            converter = get_converter(filename)
            if not converter:
                results.append({
                    'original': filename,
                    'converted': None,
                    'success': False
                })
                continue
                
            # Générer le nom de fichier de sortie
            output_filename = converter.get_output_filename(filename)
            output_path = os.path.join(app.config['CONVERTED_FOLDER'], f"{unique_id}_{output_filename}")

            file.save(raw_path)
            success = converter.convert(raw_path, output_path)

            results.append({
                'original': filename,
                'converted': f"{unique_id}_{output_filename}" if success else None,
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
