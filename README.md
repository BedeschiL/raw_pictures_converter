```
sudo apt-get install libreoffice --no-install-recommends
```

# RAW to PNG Converter Pro

Application web pour convertir des images RAW (NEF, CR2, ARW, DNG, ORF) en PNG.

## Fonctionnalités

- Interface moderne et intuitive
- Conversion par lot de fichiers RAW
- Téléchargement individuel ou groupé (ZIP)
- Architecture modulaire pour ajouter facilement d'autres convertisseurs
- Prise en charge des formats :
  - Nikon (.nef)
  - Canon (.cr2) 
  - Sony (.arw)
  - Adobe (.dng)
  - Olympus (.orf)
  - Fichiers RAW génériques (.raw)

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-repo/raw-pictures-converter.git
cd raw-pictures-converter
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Démarrer l'application :
```bash
python app.py
```

L'application sera accessible à l'adresse : `http://localhost:5000`

## Ajouter un nouveau convertisseur

1. Créer un nouveau fichier dans le dossier `converters` (ex: `png_to_svg.py`)
2. Implémenter la classe en héritant de `BaseConverter` :
```python
from .base_converter import BaseConverter

class PngToSvgConverter(BaseConverter):
    @classmethod
    def supported_formats(cls):
        return ('png',)
        
    @classmethod 
    def output_extension(cls):
        return 'svg'
        
    @classmethod
    def convert(cls, input_path, output_path):
        # Implémentation de la conversion
        pass
```

3. Enregistrer le convertisseur dans `app.py` :
```python
from converters.png_to_svg import PngToSvgConverter

CONVERTERS = {
    'raw_to_png': RawToPngConverter,
    'png_to_svg': PngToSvgConverter
}
```

## Structure du projet

```
raw-pictures-converter/
├── app.py                # Application principale
├── requirements.txt      # Dépendances
├── README.md             # Documentation
├── static/               # Fichiers statiques
│   ├── css/              # Feuilles de style
│   ├── uploads/          # Fichiers uploadés
│   └── converted/        # Fichiers convertis
├── templates/            # Templates HTML
│   └── index.html        # Page principale
└── converters/           # Modules de conversion
    ├── __init__.py       # Package converters
    ├── base_converter.py # Classe de base
    └── raw_to_png.py     # Convertisseur RAW vers PNG
```

## Dépendances

- Flask (framework web)
- Pillow (traitement d'images)
- rawpy (lecture des fichiers RAW)
- imageio (sauvegarde des images)
