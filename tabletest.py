from math import sqrt
#input is two lists of tuples

lst1 = [(255,233,100),(100,122,255),(255,183,100)]
lst2 = [(149,72,194),(254,99,200),(194,137,72)]

def ColourDiff(tup1,tup2):
    r1,g1,b1 = tup1
    r2,g2,b2 = tup2
    rChange = (r1 - r2) ** 2
    gChange = (g1 - g2) ** 2
    bChange = (b1 - b2) ** 2
    rMean = (r1 + r2) // 2
    return int(round(sqrt((2 + rMean // 256 ) * rChange + 4 * gChange + (2 + (255 - rMean) // 256) * bChange)))

def DiffTable(lst1,lst2):
    table = []
    for colour1 in lst1:
        row = []
        for colour2 in lst2:
            row += [ColourDiff(colour1, colour2)]
        table += [row]
    return table    

print(DiffTable(lst1, lst2))



