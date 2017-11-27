INPUT_FILE = "shape_of_you.txt"

sentences = list()

with open(INPUT_FILE) as file: 
   for line in file: 
      sentences.append(line.strip("\n").strip(" "))
print(sentences)

