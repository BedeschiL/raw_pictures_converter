import os
import subprocess
from .base_converter import BaseConverter

class DocxPdfConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.name = "DOCX ↔ PDF Converter"
        self.supported_formats = ['.docx', '.pdf']

    def convert(self, input_path, output_dir):
        try:
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            
            if ext.lower() == '.docx':
                output_path = os.path.join(output_dir, f"{name}.pdf")
                self.docx_to_pdf(input_path, output_path)
                return output_path
            
            elif ext.lower() == '.pdf':
                output_path = os.path.join(output_dir, f"{name}.docx") 
                self.pdf_to_docx(input_path, output_path)
                return output_path
            
            else:
                raise ValueError("Format de fichier non supporté")

        except Exception as e:
            print(f"Erreur de conversion: {str(e)}")
            raise

    def docx_to_pdf(self, input_path, output_path):
        """Convert DOCX to PDF using LibreOffice"""
        try:
            cmd = [
                'libreoffice', 
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', os.path.dirname(output_path),
                input_path
            ]
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Échec de conversion DOCX vers PDF: {str(e)}")

    def pdf_to_docx(self, input_path, output_path):
        """Convert PDF to DOCX using LibreOffice"""
        try:
            cmd = [
                'libreoffice',
                '--headless',
                '--convert-to', 'docx',
                '--outdir', os.path.dirname(output_path),
                input_path
            ]
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Échec de conversion PDF vers DOCX: {str(e)}")
