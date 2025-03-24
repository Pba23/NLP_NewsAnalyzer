import subprocess

# Télécharger le modèle spaCy français
subprocess.run(["python", "-m", "spacy", "download", "fr_core_news_md"])
