import sys

def compareStrings(strA, strB):
    currentStartIndexA = 0
    strB = strB.split("*")
    for i in strB:
        if i == "":
            continue
        currentStartIndexA = strA.find(i, currentStartIndexA)
        if currentStartIndexA == -1:
            return False
        currentStartIndexA += len(i)
    if (strA.find(strB[0]) == 0 or strB[0] == "") and (strB[-1] == "" or strB[-1] == strA[-len(strB[-1]):]) :
        return True
    else:
        return False
    
if __name__ == "__main__":
    sys.argv = sys.argv[1:]
    if not (len(sys.argv) == 2):
        print("usage")
    else:
        if(compareStrings(sys.argv[0], sys.argv[1])):
            print("OK")
        else:
            print("KO")
