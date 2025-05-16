from PIL import Image
import rawpy
import imageio
from .base_converter import BaseConverter
from typing import Tuple

class RawToPngConverter(BaseConverter):
    """Convertisseur d'images RAW vers PNG"""
    
    @classmethod
    def supported_formats(cls) -> Tuple[str, ...]:
        return ('nef', 'cr2', 'arw', 'dng', 'raw', 'orf')
        
    @classmethod
    def output_extension(cls) -> str:
        return 'png'
        
    @classmethod
    def convert(cls, input_path: str, output_path: str) -> bool:
        """
        Convertit une image RAW en PNG
        
        Args:
            input_path: Chemin du fichier RAW d'entrée
            output_path: Chemin du fichier PNG de sortie
            
        Returns:
            bool: True si la conversion a réussi, False sinon
        """
        try:
            # Traitement spécial pour les fichiers ORF
            if input_path.lower().endswith('.orf'):
                with rawpy.imread(input_path) as raw:
                    rgb = raw.postprocess()
                    imageio.imsave(output_path, rgb)
            else:
                # Traitement standard pour les autres formats RAW
                with Image.open(input_path) as img:
                    img.save(output_path, 'PNG')
            return True
        except Exception as e:
            print(f"Erreur de conversion RAW vers PNG: {e}")
            return False
