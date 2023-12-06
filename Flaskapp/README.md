# Flask
- Lancer l'exécution du Script flaskapp.py :
python3 flaskapp.py

# Sitemap
|_ APP *dossier Docker*
|_ STATIC *contient les données : images, anecdotes, etc.*
    |_ ANECDOTES *la DB des anecdotes*
        |_ abeille_anecdotes.txt
        |_ coccinelle_anecdotes.txt
        |_ papillon_anecdotes.txt
    |
    |_ ASSETS
        |_ CSS
        |_ JS
        |_ WEBFONTS
    |
    |_ DOC_CONTENT *documents téléchargeables*
        |_ impact_mapping_bloc6.drawio.xml
        |_ etc.
    |
    |_ IMAGES *dossier contenant les images du site*
        |_ banner.jpg
        |_ Etc.
    |
    |_ USER_CONTENT *dossier contenant les images envoyées sur le serveur*
        |_ Etc.
    |
    |_ favicon.ico
|
|_ TEMPLATES *dossier avec les .html*
    |_ index.html
    |_ predictions.html
    |_ gestion.html
|
|_ config.py *fichier de configuration*
|_ dictionary.txt *fichier des noms*
|_ Dockerfile
|_ flaskapp.py
|_ model.h5 *fichier contenant le modèle*
|_ README.md
|_ requirements.txt *librairies*
 