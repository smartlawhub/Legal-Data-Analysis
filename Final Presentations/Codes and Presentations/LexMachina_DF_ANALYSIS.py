import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("dark", {'axes.facecolor': 'black', 'grid.color': 'none', 'axes.edgecolor': 'white'})
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'axes.titlesize': 18,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'xtick.color': 'white',
    'ytick.color': 'white',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.left': True,
    'axes.spines.bottom': True,
    'font.family': 'sans-serif',
    'font.sans-serif': 'Lato',
})

width_px = 1180
height_px = 1080

dpi = 300

width_in = width_px / dpi
height_in = height_px / dpi

plt.figure(figsize=(width_in, height_in))
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

# Load the data
df = pd.read_csv("DF_SANCTIONS_MERGED&CLEANED.csv", delimiter=';')

sector_mapping = {
    'ÉDITION DE SYSTÈME D\'EXPLOITATION': 'Technology',
    'GESTION IMMOBILIÈRE': 'Real Estate',
    'TRADUCTION DE DOCUMENTS': 'Professional Services',
    'INTERMÉDIATION EN ASSURANCE': 'Finance',
    'INSTALLATION D\'EQUIPEMENTS D\'ISOLATION': 'Construction',
    'COMMERCE EN LIGNE': 'E-commerce',
    'COOPÉRATIVE DE COMMERCANTS DÉTAILLANTS': 'Retail',
    'BANQUE': 'Finance',
    'GRANDE DISTRIBUTION': 'Retail',
    'TRANSPORT DE VOYAGEURS PAR TAXI': 'Transportation',
    'MÉDECIN': 'Healthcare',
    'DÉMARCHAGE COMMERCIAL': 'Marketing',
    'SERVICES TECHNOLOGIQUES': 'Technology',
    'LIVRAISON DE REPAS': 'Food Services',
    'COMMERCE DE DÉTAIL D\'OPTIQUE': 'Retail',
    'DÉVELOPPEMENT DE SOLUTIONS INFORMATIQUES': 'Technology',
    'ÉDITION DE LOGICIELS APPLICATIFS': 'Technology',
    'SITE DE VENTES PRIVÉES DEDIÉ AU BRICOLAGE, AU JARDINAGE ET À L\'AMÉNAGEMENT DE LA MAISON': 'E-commerce',
    'ASSURANCE': 'Finance',
    'BIOTECHNOLOGIES AGRICOLES': 'Biotechnology',
    'PRESSE': 'Media',
    'RÉGIE PUBLICITAIRE': 'Advertising',
    'NOTAIRE': 'Legal Services',
    'ETABLISSEMENT PUBLIC A CARACTERE INDUSTRIEL ET COMMERCIAL': 'Public Sector',
    'ETABLISSEMENT DE PAIEMENT': 'Finance',
    'OPERATION DE TELEPHONIE': 'Telecommunications',
    'VENTE DE MOBILIER SUR INTERNET ET EN MAGASIN': 'E-commerce',
    'RESEAU SOCIAL': 'Social Media',
    'SERVICES INTERNET (MOTEUR DE RECHERCHE, PLATEFORME DE VIDEOS, ETC.)': 'Technology',
    'ENTRETIEN ET DE REPARATION DE VEHICULES AUTOMOBILES': 'Automotive Services',
    'RESTAURANT': 'Food Services',
    'FOURNITURE ET PRODUCTION D\'ELECTRICITE ET DE GAZ': 'Energy',
    'LOCATION DE VEHICULES': 'Transportation',
    'HOTELLERIE': 'Hospitality',
    'GREFFES DE TRIBUNAUX DE COMMERCE DE FRANCE': 'Legal Services',
    'DEVELOPPEMENT DE LOGICIEL DE RECONNAISSANCE FACIALE': 'Technology',
    'DEVELOPPEMENT DE LOGICIEL DE VOIX SUR IP ET UNE MESSAGERIE INSTANTANEE': 'Technology',
    'FOURNITURE D\'ELECTRICITE, DE GAZ ET DE SERVICES': 'Energy',
    'OPERATION DE TELECOMMUNICATION FIXE': 'Telecommunications',
    'VENTE DE SYSTEMES D’EXPLOITATION, DE LOGICIELS APPLICATIFS, DE MATERIELS ET DE SERVICES DERIVES': 'Technology',
    'UNIVERSITE': 'Education',
    'DEVELOPPEMENT DE LOGICIELS DE GESTION ET LA COMMERCIALISATION DE LOGICIELS A DESTINATION DES COLLECTIVITES TERRITORIALES': 'Technology',
    'DEVELOPPEMENT DE JEUX MOBILES': 'Gaming',
    'PLATEFORMES DE DISTRIBUTION DE CONTENUS': 'Media',
    'CREATION ET COMMERCIALISATION DE PRODUITS ELECTRONIQUES GRAND PUBLIC, DES ORDINATEURS PERSONNELS ET DES LOGICIELS': 'Technology',
    'CONSEIL EN SYSTEMES ET LOGICIELS INFORMATIQUES': 'Technology Consulting',
    'COMMUNE': 'Public Sector',

}

# Apply the sector mapping to create a new 'Broad_Sector' column
df['Broad_Sector'] = df['Secteur d\'activité'].map(sector_mapping).fillna('Other')

# Normalize entity names and create 'Normalized_Entite' column
df['Normalized_Entite'] = df['Nom_Entite'].str.upper().str.strip()

# Convert 'Montant_Amende' to string and handle non-numeric values
df['Montant_Amende'] = df['Montant_Amende'].astype(str).str.replace('NEANT', 'NaN')

# Convert 'Montant_Amende' to a numeric type, coercing errors to NaN
df['Montant_Amende'] = pd.to_numeric(df['Montant_Amende'].str.replace(',', '.'), errors='coerce')

# Convert 'Date' to datetime and extract the year
df['Year'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.year

# Temporal analysis of the number of sanctions over the years
sanctions_per_year = df.groupby('Year').size()

# Temporal analysis of the types of procedures used
procedures_per_year = df.groupby(['Year', 'Type de procédure']).size().unstack(fill_value=0)

# Analysis of the recurrence of sanctions
most_sanctioned_entities = df['Normalized_Entite'].value_counts().head(5)
most_sanctioned_sectors = df['Broad_Sector'].value_counts().head(5)

# Financial analysis
fine_stats = df['Montant_Amende'].describe()

# Group by normalized entity names and sum the fines
entities_total_fines = df.groupby('Normalized_Entite')['Montant_Amende'].sum().reset_index()
entities_highest_fines = entities_total_fines.sort_values(by='Montant_Amende', ascending=False).head(5)

# Identification of sectors with the highest total fine amount
sectors_highest_fines = df.groupby('Broad_Sector')['Montant_Amende'].sum().nlargest(5)

# Analysis of the most frequent shortcomings
shortcomings = df['Manquements'].str.split('\n').explode().value_counts().head(5)

# Data Visualization :

# a. Number of sanctions issued by the CNIL each year since 2019
plt.figure(figsize=(10, 6))
sanctions_per_year.plot(kind='bar', color='white')
plt.title('Number of Sanctions Over the Years')
plt.xlabel('Year')
plt.ylabel('Number of Sanctions')
plt.tight_layout()
plt.savefig('a-Number of sanctions issued by the CNIL each year since 2019.png', facecolor='black', dpi=dpi, bbox_inches='tight')

# b. Top 5 most frequently sanctioned Industries
plt.figure(figsize=(10, 6))
most_sanctioned_sectors.plot(kind='barh', color='white')
plt.xlabel('Number of Sanctions')
plt.ylabel('Sector')
plt.tight_layout()
plt.savefig('b-Top 5 most frequently sanctioned Industries.png', facecolor='black', dpi=dpi, bbox_inches='tight')

# c. Types of procedures used
plt.figure(figsize=(10, 6))
procedures_per_year.plot(kind='bar', stacked=True, color=['white', 'grey'])
plt.xlabel('Year')
plt.ylabel('Number of Procedures')
plt.tight_layout()
plt.savefig('c-Types of procedures used.png', facecolor='black', dpi=dpi, bbox_inches='tight')

# d. Top 5 Industries with the highest fines
plt.figure(figsize=(10, 6))
sectors_highest_fines.plot(kind='barh', color='white')
plt.xlabel('Total Fine Amount (in millions €)')
plt.ylabel('Sector')
plt.gca().get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:.2f}M".format(x/1e6)))
plt.tight_layout()
plt.savefig('d-Top 5 Industries with the highest fines.png', facecolor='black', dpi=dpi, bbox_inches='tight')

# e. Top 5 entities with the highest fines
plt.figure(figsize=(10, 6))
entities_highest_fines.plot(kind='barh', x='Normalized_Entite', y='Montant_Amende', color='white')
plt.xlabel('Total Fine Amount (in millions €)')
plt.ylabel('Entity Name')
plt.gca().get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:.2f}M".format(x/1e6)))
plt.tight_layout()
plt.savefig('e-Top 5 entities with the highest finess.png', facecolor='black', dpi=dpi, bbox_inches='tight')

# f. Top 5 most frequent breaches
plt.figure(figsize=(10, 6))
shortcomings.plot(kind='barh', color='white')
plt.xlabel('Frequency')
plt.ylabel('Shortcoming')
plt.tight_layout()
plt.savefig('f-Top 5 most frequent breaches.png', facecolor='black', dpi=dpi, bbox_inches='tight')

print("Data analysis and visualization completed.")