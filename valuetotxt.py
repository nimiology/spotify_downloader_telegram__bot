def savetxt(txt):
    with open("vakues.txt",'w+') as file:
        file.write(txt)

def read(line):
    with open("vakues.txt",'r') as file:
        text =file.readlines()[line]
        return text[:len(text)-1]