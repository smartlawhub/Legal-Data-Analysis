from judilibre import *
from pandas import read_csv
import os

FILENAME = "test100" # Nom du fichier csv générant les données
NB_TEXTE_PAR_COUR = 100 # Nombre de textes à récupérer par cour
STEP_ANALYSE = 100  

async def main():
    # Créé le fichier csv si il n'existe pas déjà sinon récupère le contenu déjà traité
    if not os.path.isfile(FILENAME+".csv"):  
        with open(FILENAME+".csv", 'w') as file:
            file.write("id,ca,delai\n")

    csv_data = read_csv(FILENAME+".csv")


    villes = get_locations() # Cours d'appel
    villes["cc"] = "Cour de cassation"
    for v in villes :
        print("\n" + v + " : Récupération des textes")

        # Requête différente si cour de cassation ou cour d'appel
        if v == "cc":
            ids = get_decisions_ids("délai raisonnable", "cc", page_size=50, stop_at=NB_TEXTE_PAR_COUR)
        else:
            ids = get_decisions_ids("délai raisonnable", "ca", v, page_size=50, stop_at=NB_TEXTE_PAR_COUR)
        total = len(ids)

        print("\n" + v + " : Analyse des textes")

        # Analyse les textes en plusieurs fois pour pas surcharger le serveur
        step = 100 
        start = 0
        end = step
        while end - step <= total:
            slice_ids = ids[start:end]

            texts_dict = await get_texts_async(slice_ids)
            texts = [t["text"] for t in texts_dict]
            
            for i, id in enumerate(slice_ids):
                print(f"{v} : {i+1+start}/{total}")

                # Si texte déjà traité (déjà dans le csv) ne prends pas en compte ce texte
                if id in csv_data['id'].values:
                    print("Texte déjà traité")
                    continue

                # Récupère la moyenne des délais mentionnés dans le texte
                delai = delai_raisonnable(texts[i])

                # Ajoute dans le csv
                with open(FILENAME+".csv", 'a') as file:
                    file.write(f'{id},{v},{delai}\n')

            start = end
            end = start + step

asyncio.run(main())