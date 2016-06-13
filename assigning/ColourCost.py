from math import sqrt

def ColourDiff(tup1,tup2):
    
    r1,g1,b1 = tup1
    r2,g2,b2 = tup2
    rChange = (r1 - r2) ** 2
    gChange = (g1 - g2) ** 2
    bChange = (b1 - b2) ** 2
    rMean = (r1 + r2) // 2
    
    return int(round(sqrt((2 + rMean // 256 ) * rChange + 4 * gChange + (2 + (255 - rMean) // 256) * bChange)))

def DiffTable(filename):
    
    lstoflst = []
    table = []
    fh = open(filename, 'r')
    
    for line in fh:
        if line == '[\n':
            lst = []
            lstart = True
        elif line == ']\n':
            lstoflst += [lst]
        elif lstart:
            tup = ([int(x) for x in line.split()])
            lst += [tup]
    
    for colour1 in lstoflst[0]:
        row = []
        for colour2 in lstoflst[1]:
            row += [ColourDiff(colour1, colour2)]
        table += [row]
    return table    

# print(DiffTable(lst1, lst2))


def TupToFile(lst, filename):
    # gets a list of tuples 'lst' and writes them into the file 'filename'
    # in the format we use up in DiffTable
    oh = open(filename, "w")
    oh.write("[\n")
    for tup in lst:
        oh.write("%i %i %i \n" %(tup[0], tup[1], tup[2]))
    oh.write("]\n")    
