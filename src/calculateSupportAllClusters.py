'''
Created on 2 Aug 2017

@author: user
'''

dataTranspose = dict()
dataset = list() #list of list of set

def subseqChecker(subseq,seq):
    seqSize = len(seq)
    subSize = len(subseq)
    if subSize > seqSize:
        return False
    isSubset = False
    itemsetCounter = 0
    itemset = subseq[itemsetCounter]
    for i in range(0,seqSize):
        if seq[i].issuperset(itemset):
            itemsetCounter += 1
            if itemsetCounter == subSize:
                isSubset = True
                break
            itemset = subseq[itemsetCounter]
    return isSubset

def supportCalculatorLong(subseq):
    if len(subseq) == 0:
        return len(dataset)
    support = 0
    for seq in dataset:
        if subseqChecker(subseq, seq):
            support += 1
    return support

def supportCalculator(subseq):
    if len(subseq) == 0:
        return len(dataset)
    setOfItems = set()
    support=0
    commonTransactions = set()
    filled = False
    for it in subseq:
        for i in it:
            if i not in setOfItems:
                if filled:
                    commonTransactions = commonTransactions.intersection(dataTranspose[i])
                else:
                    commonTransactions = dataTranspose[i]
                    filled=True
                setOfItems.add(i)
    
    for c in commonTransactions:
        if subseqChecker(subseq, dataset[c]):
            support += 1
    return support

def lineToSeq(lineInput,lineNum):
    returnSeq = list()
    itemset = set()
    splitResult = lineInput.split(' ')
    itemsetNum = 0
    for subStr in splitResult:
        if subStr=='-1':
            returnSeq.append(itemset)
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

index = 0
datasetFile = 'dataset/cluster15.txt'
toBeCalculated = 'dataset/smallCalc.txt'
with open(datasetFile) as openfileobject:
    for line in openfileobject:
        seq = lineToSeq(line,index)
        dataset.append(seq)
        index += 1
        
fOut = open('dataset/supportsFromCluster.txt','w')
with open(toBeCalculated) as openfileobject:
    for line in openfileobject:
        line = line.split(' #')[0]
        returnSeq = list()
        itemset = set()
        splitResult = line.split(' ')
        itemsetNum = 0
        inCluster = True
        for subStr in splitResult:
            if subStr=='-1':
                returnSeq.append(itemset)
                itemset = set()
                itemsetNum += 1
            else:
                if subStr not in dataTranspose.keys():
                    inCluster = False
                itemset.add(subStr)
        if not inCluster:
            fOut.write('0\n')
        else:
            fOut.write(str(supportCalculator(returnSeq)) + '\n')
fOut.close()