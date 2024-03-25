import pandas as pd
import matplotlib.pyplot as plt

# Nom du fichier csv 
FILENAME = "test100"

data = pd.read_csv(FILENAME+".csv")
data = data[data["delai"] != -1] # Retire du dataframe les textes où aucun délai n'a été trouvé
print(data.head())

data = data.groupby("ca")["delai"].describe()

print(data)