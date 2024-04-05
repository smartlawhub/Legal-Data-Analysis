import pandas as pd

def fusionner_fichiers_csv(chemin_legifrance, chemin_cnil, chemin_sortie, format_date='%d/%m/%Y'):
   
    df_legifrance = pd.read_csv(chemin_legifrance)
    df_cnil = pd.read_csv(chemin_cnil)

    df_legifrance.columns = ['Numero_Sanction', 'Date', 'Type_Entite', 'Nom_Entite', 'Montant_Amende', 'Articles_RGPD', 'Articles_LIL']
    df_cnil.columns = ['Date', 'Secteur d\'activité', 'Manquements', 'Montant_Amende']

    df_legifrance['Date'] = pd.to_datetime(df_legifrance['Date'], errors='coerce', format=format_date)
    df_cnil['Date'] = pd.to_datetime(df_cnil['Date'], errors='coerce', format=format_date)

    df_legifrance['Montant_Amende'] = pd.to_numeric(df_legifrance['Montant_Amende'], errors='coerce')
    df_cnil['Montant_Amende'] = pd.to_numeric(df_cnil['Montant_Amende'], errors='coerce')

    df_merged = pd.merge(df_legifrance, df_cnil[['Date', 'Montant_Amende', 'Secteur d\'activité', 'Manquements']], 
                         on=['Date', 'Montant_Amende'], 
                         how='outer', 
                         suffixes=('', '_cnil'))

    df_merged.to_csv(chemin_sortie, index=False, date_format=format_date)

chemin_legifrance = '/Users/Edouard Tan/LDA/DF_LEGIFRANCE_CLEANED.csv'
chemin_cnil = '/Users/Edouard Tan/LDA/DF_CNIL_CLEANED.csv'
chemin_sortie = '/Users/Edouard Tan/LDA/DF_SANCTIONS_MERGED.csv'
format_date = '%d/%m/%Y'

fusionner_fichiers_csv(chemin_legifrance, chemin_cnil, chemin_sortie, format_date)
