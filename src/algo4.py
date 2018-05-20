'''
Created on 30 May 2017

@author: user
'''
import random
from _operator import itemgetter

dataTranspose = dict()
dataset = list()

def inclusionExclusionAllCommonSequenceS1(position,m,level,temp,L,LPosition,d):
    x = 0
    if level==0:
        x = (2**len(temp) - 1) * d[LPosition[position]][m]
    else:
        for j in range(position-1,-1,-1):
            temp1 = set(L[j])
            temp1 = temp1.intersection(temp)
            if len(temp1) > 0:
                level -= 1
                x += inclusionExclusionAllCommonSequenceS1(j,m,level,temp1,L,LPosition,d)
                level += 1
    return x

def inclusionExclusionAllCommonSequenceS1S2(position,level,temp,Lx,Ly,LxPosition,LyPosition,d):
    itemRemove = 0
    if level==0:
        itemRemove1 = 0
        if len(temp) == 0:
            return 0
        oneL = 1
        for levelL in range(0,len(Ly)):
            for jL in range(len(Ly)-1,-1,-1):
                item = set(Ly[jL])
                item = item.intersection(temp)
                if len(item) != 0:
                    itemRemove1 += oneL * inclusionExclusionAllCommonSequenceS1(jL,LxPosition[position],levelL,item,Ly,LyPosition,d)
            oneL = oneL * -1
        return itemRemove1
    else:
        for j in range(position-1,-1,-1):
            temp1 = set(Lx[j])
            temp1 = temp1.intersection(temp)
            if len(temp1) != 0:
                level -= 1
                itemRemove += inclusionExclusionAllCommonSequenceS1S2(j,level,temp1,Lx,Ly,LxPosition,LyPosition,d)
                level += 1
    return itemRemove

def generateL(endSeq,S,itemN,positionSet):
    L = list()
    for k in range(0,endSeq+1):
        intersection = itemN.intersection(S[k])
        if len(intersection) > 0:
            # add_element - START
            i = 0
            size = len(L)
            while i<size:
                if intersection.issuperset(L[i]):
                    del positionSet[i]
                    del L[i]
                    size -= 1
                else:
                    i += 1
            L.append(set(intersection))
            positionSet.append(k)
            # add_element - FINISH
    return L

def prepareMatrix(n,m):
    d = list()
    d2 = list()
    for j in range(0,m+1):
        d2.append(1)
    d.append(list(d2))
    d2.clear()
    d2.append(1)
    for j in range(1,m+1):
        d2.append(0)
    for i in range(1,n+1):
        d.append(list(d2))
    return d

def acs(seq1, seq2):
    if (len(seq1)==0 or len(seq2)==0):
        return 1
    seqLength1 = len(seq1)
    seqLength2 = len(seq2)
    d = prepareMatrix(seqLength1, seqLength2)
    for i in range(0,seqLength1):
        for j in range(0,seqLength2):
            x = seq2[j]
            Ly = list()
            Lx = list()
            LyPosition = list()
            LxPosition = list()
            Ly = generateL(i,seq1,x,LyPosition)
            itemRemove = 0
            one = 1
            A = 0
            R = 0
            for levely in range(0,len(Ly)):
                for jj in range(len(Ly)-1,-1,-1):
                    item = set(Ly[jj])
                    itemRemove += inclusionExclusionAllCommonSequenceS1(jj,j,levely,item,Ly,LyPosition,d)
                A += one*itemRemove
                itemRemove = 0
                one = one * -1
            if len(Ly) != 0:
                Lx = generateL(j-1, seq2, x, LxPosition)
                oneXY = 1
                itemRemove = 0
                for levelx in range(0,len(Lx)):
                    for jG in range(len(Lx)-1,-1,-1):
                        itemG = set(Lx[jG])
                        itemRemove += inclusionExclusionAllCommonSequenceS1S2(jG,levelx,itemG,Lx,Ly,LxPosition,LyPosition,d)
                    R += oneXY * itemRemove
                    itemRemove = 0
                    oneXY = oneXY * -1
            d[i+1][j+1] = d[i+1][j] + A - R
    return d[len(d)-1][len(d[0])-1]

def lineToSeq(lineInput,lineNum):
    returnSeq = list()
    itemset = set()
    splitResult = lineInput.split(' ')
    itemsetNum = 0
    for subStr in splitResult:
        if subStr=='-1':
            returnSeq.append(set(itemset))
            itemset = set()
            itemsetNum += 1
        elif subStr=='-2\n' or subStr=='-2':
            return returnSeq
        else:
            itemset.add(subStr)
            if (subStr not in dataTranspose.keys()):
                dataTranspose[subStr] = {lineNum}
            else:
                dataTranspose[subStr].add(lineNum)
    return returnSeq

def weightedChoice(choices,total):
    r = random.uniform(0, total)
    #print('random number :',r)
    upto = 0
    for c1, c2, w in choices:
        if upto + w >= r:
            return c1,c2
        upto += w
        
sequ1 = list([set(['a']),set(['a','b']),set(['e']),set(['c','d']),set(['b','d'])])
sequ2 = list([set(['a']),set(['b','c','d']),set(['a','d'])])

filename = 'small'
index = 0
with open(filename + '.txt') as openfileobject:
    for line in openfileobject:
        seq = lineToSeq(line,index)
        dataset.append(list(seq))
        index += 1

listOfPairs = list()
totalWeight = 0
for di in range(0,len(dataset)):
    for dj in range(di+1,len(dataset)):
        weight = acs(dataset[di], dataset[dj])
        totalWeight += weight
        listOfPairs.append((di, dj, weight))
orderedWeight = sorted(listOfPairs, key=itemgetter(2), reverse=True)
print(orderedWeight)

for i in range(0,10):
    chosenPair = weightedChoice(orderedWeight,totalWeight)
    print(chosenPair)
