from abc import ABC, abstractmethod
from typing import Tuple
import os

class BaseConverter(ABC):
    """Classe de base pour tous les convertisseurs d'images"""
    
    @classmethod
    @abstractmethod
    def supported_formats(cls) -> Tuple[str, ...]:
        """Retourne les extensions de fichiers supportées"""
        pass
        
    @classmethod
    @abstractmethod
    def convert(cls, input_path: str, output_path: str) -> bool:
        """
        Convertit le fichier d'entrée vers le format de sortie
        
        Args:
            input_path: Chemin du fichier d'entrée
            output_path: Chemin du fichier de sortie
            
        Returns:
            bool: True si la conversion a réussi, False sinon
        """
        pass
    
    @classmethod
    def get_output_filename(cls, input_filename: str) -> str:
        """
        Génère le nom de fichier de sortie basé sur le fichier d'entrée
        
        Args:
            input_filename: Nom du fichier d'entrée
            
        Returns:
            str: Nom du fichier de sortie
        """
        base_name = os.path.splitext(input_filename)[0]
        return f"{base_name}.{cls.output_extension()}"
    
    @classmethod
    @abstractmethod
    def output_extension(cls) -> str:
        """Retourne l'extension du fichier de sortie"""
        pass
