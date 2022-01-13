import re
import os

# os.chdir("./Lesson1/Manipulating Files")

print(os.listdir("."))  # We check what files are in the folder
file = "Empty File is Empty.txt"  # We select a file that is in the folder and attribute it to a variable
newnamefile = file + "a"  # We decide on a new name given a file
os.rename(file, newnamefile)
os.rename(newnamefile, newnamefile[:-1])

answer = 0

os.chdir("../Data Storage/Gibberish")
for file in os.listdir("."):
    if re.search("_\d\d?.txt", file) is None:
        # os.rename(file, file[:-4] + "_main" + ".txt")
        answer += 1
print(answer)
