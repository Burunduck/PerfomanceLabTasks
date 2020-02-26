import sys

def isDataCorrect(nb, baseSrc, baseDst):
    return False if len(nb) == 0 or len(baseSrc) == 0 or len(set(baseDst)) != len(baseDst) or len(set(nb).union(set(baseSrc))) != len(baseSrc) else True

def itoBaseTen(nb, baseSrc):
    baseTen = [baseSrc.index(x) for x in reversed(nb)]
    for i in range(len(baseTen)):
        baseTen[i] *= len(baseSrc) ** i
    return sum(baseTen)

def itoBaseDst(nb, baseDst):
    alphabet = baseDst
    baseDst = len(baseDst)
    nbInNewBase = []
    while(nb >= baseDst):
         nbInNewBase.append(nb % baseDst)
         nb //= baseDst
    nbInNewBase.append(nb)
    return "".join([alphabet[x] for x in reversed(nbInNewBase)])

def itoBase(nb, base, baseDst = None):
    if  isinstance(baseDst, str):
        if not isDataCorrect(nb, base, baseDst):
            return "usage"
        nb = itoBaseTen(nb, base)
        return str(itoBaseDst(nb, baseDst))
    else:
        if not isDataCorrect(str(nb), base, ""):
            return "usage"
        return str(itoBaseDst(int(nb), base))

if __name__ == "__main__":
    sys.argv = sys.argv[1:]
    if len (sys.argv) == 2:
        nb = sys.argv[0]
        base = sys.argv[1]
        print(itoBase(nb, base))
    elif len (sys.argv) == 3:
        nb = sys.argv[0]
        base = sys.argv[1]
        baseDst = sys.argv[2]
        print(itoBase(nb, base, baseDst))
    elif len (sys.argv) > 3 or len (sys.argv) < 2:
        print ("usage")
        sys.exit (1)



