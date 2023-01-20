import pandas as pd
import regex as re

f = open("..Data/poem.txt", "r", encoding="latin1")
poem = f.read()
df = pd.DataFrame()  # Fill with df that has students' handles

#Exo 1




# In this exercise, you will need to find the number of words that are common to two paragraphs of the poems. The paragraphs are: There are (at least) three steps to do so, and every method is indicated in the lesson 1c Functions and Methods. Remember, in particular, that the function set() can create a set from a list.

dd = {{1: 'freckled and frivolous cake there was\nThat sailed upon a pointless sea, \nOr any lugubrious lake there was\nIn a manner emphatic and free.\nHow jointlessly, and how jointlessly\nThe frivolous cake sailed by\nOn the waves of the ocean that pointlessly\nThrew fish to the lilac sky.',
 2: ' Oh, plenty and plenty of hake there was\nOf a glory beyond compare, \nAnd every conceivable make there was\nWas tossed through the lilac air.',
 3: ' Up the smooth billows and over the crests\nOf the cumbersome combers flew\nThe frivolous cake with a knife in the wake\nOf herself and her curranty crew.\nLike a swordfish grim it would bounce and skim\n(This dinner knife fierce and blue) , \nAnd the frivolous cake was filled to the brim\nWith the fun of her curranty crew.',
 4: ' Oh, plenty and plenty of hake there was\nOf a glory beyond compare -\nAnd every conceivable make there was\nWas tossed through the lilac air.',
 5: ' Around the shores of the Elegant Isles\nWhere the cat-fish bask and purr\nAnd lick their paws with adhesive smiles\nAnd wriggle their fins of fur, \nThey fly and fly neath the lilac sky -\nThe frivolous cake, and the knife\nWho winketh his glamorous indigo eye\nIn the wake of his future wife.',
 6: ' The crumbs blow free down the pointless sea\nTo the beat of a cakey heart\nAnd the sensitive steel of the knife can feel\nThat love is a race apart\nIn the speed of the lingering light are blown\nThe crumbs to the hake above, \nAnd the tropical air vibrates to the drone\nOf a cake in the throes of love.'}}

TT = ""
for index, row in df.loc[df.Type == "DMI"].iterrows():
     TT = ""
     TT += "# In this exercise, you will need to find the number of words that are common to two paragraphs of the poems. The paragraphs are:\n\na = '"
     spls = row["Condition"].split(",")
     TT += dd[int(spls[0])].strip().replace('\n','\\n') + "'\nb = '"
     TT +=  dd[int(spls[1])].strip().replace('\n','\\n') + "'\n\n"
     TT += "# There are (at least) three steps to do so, and every method is indicated in the lesson 1c Functions and Methods. Remember, in particular, that the  function set() can create a set from a list."
     seta = set(dd[int(spls[0])].strip().split(" "))
     setb = set(dd[int(spls[1])].strip().split(" "))
     answer = len(seta.intersection(setb))
     with open(row["Handle PA"] + " - Exercise1.py", "w") as f:
         f.write(TT)
     print(answer)

# bash = for homedir in /home/!(DamienCh); do     cp "${homedir##*/} - Exercise1.py" $homedir/LDA/Scripts; done


#Exo 2


key = "DMI"
python = TT = ""
for index, row in df.loc[df.Type == key].iterrows():
     most = 0
     mostl = ""
     for line in poem.split("\n"):
              var = len(re.findall(row["Condition"] + "(?!=" + row["Excluded"].split(row["Condition"])[-1] + ")", line))
              if var > most:
                  most = var
                  mostl = line[:3]
     answer = most
     TT = ""
     TT += '# In this exercise, you need to identify the line number (e.g., "1.1", or "5.4") of the poem line that meets this condition:\n\n#Which line has '
     TT += str(answer) + " letters '" + row["Condition"] + "', not counting when that letter is in the word " + row["Excluded"]
     TT += "\n\n# If several lines meet this condition, indicate only the first one. This will require you to use loops, conditions, regexes, and some functions such as len(). (Or maybe not, there are plenty of ways to do it.). \n#Your will need to load the poem with the code below, and you final answer should be a va riable called 'answer' \n#that has the line number (of the format \d.\d - see the regex module). Remember that you can index a string."
     TT += '\n\nf = open("../Data/poem.txt", "r", encoding="latin1")\npoem = f.read()'
     most = 0
     mostl = ""
     for line in poem.split("\n"):
         var = len(re.findall(row["Condition"] + "(?!=" + row["Excluded"].split(row["Condition"])[-1] + ")", line))
         if var > most:
             most = var
             mostl = line[:3]
     answer = most, mostl
     df.at[index, "Answer"] = answer
     handle = row["Handle PA"]
     with open(handle  + " - Exercise2.py", "w") as f:
         f.write(TT)
     print(answer)
df.to_csv("Students.csv", index=False)

# bash = for homedir in /home/!(DamienCh); do     cp "${homedir##*/} - Exercise1.py" $homedir/LDA/Scripts; done

# Exo 3, with df being a df made from the XML files

import random
students = pd.read_csv("Students.csv", header="infer")
key = "SFJI"
handles = students.loc[students.Type == key]["Handle PA"].values.tolist()
ii = 0
L = []
while ii < 40:
    print(ii)
    veto_col = ["Type_Decision", "Numero_Dossier"]
    first_col = random.choice([x for x in df.columns if x not in veto_col])
    veto_col.append(first_col)
    first_value = random.choice(df.loc[df[first_col] != "N/A"][first_col].values.tolist())
    selec = df.loc[df[first_col] == first_value]
    second_col = random.choice([x for x in df.columns if x not in veto_col])
    veto_col.append(second_col)
    second_value = random.choice(selec.loc[selec[second_col] != "N/A"][second_col].values.tolist())
    subselec = selec.loc[selec[second_col] == second_value]
    third_col = random.choice([x for x in df.columns if x not in veto_col])
    third_value = random.choice(subselec.loc[subselec[third_col] != "N/A"][third_col].values.tolist())
    results = subselec.loc[subselec[third_col] == third_value]
    print(first_col, second_col, third_col, len(results))
    if len(results) < 6:
     TT = ""
     TT = '# In this exercise, you need to identify the decision ID (in "Numero_Dossier") of the file(s) that meets these conditions:\n"'
     TT += first_col + '" == "' + first_value + '", "' + second_col +  '" == "' + second_value + '", "' + third_col + '" == "' + third_value + '"'
     TT += "\n\n# You will need to look in every XML file, and locate the elements that have the required data for the relevant elements \n# Use the code below to land directly in the relevant folder and import relevant packages"
     TT += '\n\nimport os\nfrom lxml import etree\n\nos.chdir("../Data/CE")'
     with open(handles[ii]  + " - Exercise2.py", "w") as f:
         f.write(TT)
     L.append([handles[ii], "|".join(results["Numero_Dossier"].values.tolist())])
     ii += 1
pd.DataFrame(L).to_csv("Results.csv") # To get the results and input them in master file
