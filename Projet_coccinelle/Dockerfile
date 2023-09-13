# Utilisez l'image de base Python
FROM python:3.9

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances et l'application dans le conteneur
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Expose le port sur lequel l'application Flask s'exécute
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "flaskapp.py"]