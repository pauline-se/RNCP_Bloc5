# Image de base Python
FROM python:3.9

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie le contenu du répertoire de projet Flask dans le conteneur
COPY ./Flaskapp /app

# Copie les fichiers de dépendances et l'application dans le conteneur
RUN pip install -r requirements.txt

# Expose le port sur lequel l'application Flask s'exécute
EXPOSE 2024

# Commande pour lancer l'application
CMD ["python", "flaskapp.py"]