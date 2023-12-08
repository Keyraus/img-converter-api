from fastapi import FastAPI
import ffmpeg
import random
import string
import requests
app = FastAPI()

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def compress_to_jpegxl(input_path, output_path):
    try:
        ffmpeg.input(input_path).output(output_path, vcodec='libjxl').run()
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e 

@app.get("/compression")
def image(url = None):  
    if url is None:
       return (f"Aucun URL d'image dans la requete {url}")
    downloaded_file = (f"./{get_random_string(12)}")
    out =  telecharger_image(url=url, destination=f"{downloaded_file}.in")
    compress_to_jpegxl(f"{downloaded_file}.in", f"{downloaded_file}.jxl")
    return out

def telecharger_image(url, destination):
    try:
        # Effectuer une requete GET pour recuperer le contenu de l'image
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}        
        reponse = requests.get(url, stream=True, headers=headers)

        # Verifier si la requete a reussi (statut 200 OK)
        if reponse.status_code == 200:
            # Ecrire le contenu de l'image dans un fichier local
            with open(destination, 'wb') as fichier_local:
                for morceau in reponse.iter_content(chunk_size=128):
                    fichier_local.write(morceau)
            return f"L'image a ete telechargee avec succes vers {destination}"
        else:
            return (f"Erreur lors de la requete. Code de statut : {reponse.status_code}")
    except Exception as e:
        return(f"Une erreur s'est produite : {e}") 