import subprocess
import os

class Converter:
    @staticmethod
    def convert_to_pdf(inputfile, outputfiledir):
        try:
            # Usa una lista di argomenti invece di una stringa
            command = [
                'soffice', 
                '--headless',  # Esegue LibreOffice in modalità headless (senza GUI)
                '--convert-to', 'pdf', 
                '--outdir', outputfiledir, 
                inputfile
            ]
            
            # Esegui il comando e cattura l'output
            subprocess.run(command, check=True)
            return None  # Nessun errore
        except subprocess.CalledProcessError as e:
            return f"Conversion failed: {str(e)}"
        except FileNotFoundError:
            return "LibreOffice (soffice) not found. Please ensure it is installed and in your system's PATH."
