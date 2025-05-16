from .base_converter import BaseConverter
from typing import Tuple

class DocxToPdfConverter(BaseConverter):
    """Convertisseur DOCX vers PDF"""
    
    @classmethod
    def supported_formats(cls) -> Tuple[str, ...]:
        return ('docx',)
        
    @classmethod
    def output_extension(cls) -> str:
        return 'pdf'
        
    @classmethod
    def convert(cls, input_path: str, output_path: str) -> bool:
        """
        Convertit un fichier DOCX en PDF en utilisant LibreOffice
        
        Args:
            input_path: Chemin du fichier DOCX d'entrée
            output_path: Chemin du fichier PDF de sortie
            
        Returns:
            bool: True si la conversion a réussi, False sinon
        """
        import subprocess
        try:
            # Conversion avec LibreOffice en ligne de commande
            result = subprocess.run([
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', os.path.dirname(output_path),
                input_path
            ], capture_output=True, text=True)
            
            # Renommer le fichier de sortie
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            temp_output = os.path.join(os.path.dirname(output_path), f"{base_name}.pdf")
            if os.path.exists(temp_output):
                os.rename(temp_output, output_path)
                return True
            return False
        except Exception as e:
            print(f"Erreur de conversion: {e}")
            return False
