import math

def count(num):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    letterDigits = [0] #Count from nothing
    for _ in range(num):
        #Increment
        letterDigits[0] = letterDigits[0] + 1

        for j in range(len(letterDigits)):
            if letterDigits[j] > len(letters):
                letterDigits[j] = 1

                if j+1 < len(letterDigits): #check If there is a digit ahead based on length of letterDigits +1, since 1 based, increment it, otherwise create one
                    letterDigits[j+1] = letterDigits[j+1] + 1
                else:
                    letterDigits.append(1)

    #Convert to letter
    lettersText = ""
    for i in range(len(letterDigits)):
        lettersText += (letters[letterDigits[i] - 1])

    print(lettersText)

for i in range(10000):
    count(i+ 1)