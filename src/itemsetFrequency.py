'''
Created on 10 Mar 2017

@author: user
'''

import math
import random
import time

startTime = time.time()

dataset = list()
weights = list()
dataTranspose = dict()

def lineToItemset(lineInput): #read sequences in SPMF format, and treat them as itemsets
    returnSet = set()
    splitResult = lineInput.split(' ')
    for subStr in splitResult:
        if subStr!='-1' and subStr!='-2\n' and subStr!='-2':
            returnSet.add(subStr)
    return returnSet

def csvToItemset(lineInput,lineNum):
    returnSet = set()
    splitResult = lineInput.split(',')
    numAtt = len(splitResult)
    attCount = 0
    for subStr in splitResult:
        attCount += 1
        if subStr=='?' or attCount==numAtt:
            continue
        subStr = subStr.replace("'","")
        subStr = subStr.replace("\\","")
        item = str(attCount) + '-' + subStr
        returnSet.add(item)
        if (item not in dataTranspose.keys()):
            dataTranspose[item] = {lineNum}
        else:
            dataTranspose[item].add(lineNum)
    return returnSet

def selectRandomSubset(itemset):
    subset = set()
    for item in itemset:
        r = random.getrandbits(1)
        if r:
            subset.add(item)
    return subset    

def supportCalculatorLong(dataset,subset):
    if len(subset) == 0:
        return len(dataset)
    support = 0
    for d in dataset:
        if d.issuperset(subset):
            support += 1
    return support

def supportCalculator(subset):
    if len(subset) == 0:
        return len(dataset)
    commonTransactions = set()
    filled = False
    for i in subset:
        if filled:
            commonTransactions = commonTransactions.intersection(dataTranspose[i])
        else:
            commonTransactions = dataTranspose[i]
            filled=True
    return len(commonTransactions)

def weightedChoice(choices,total):
    #total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    #print('random number :',r)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w

totalWeight = 0
index = 0
filename = 'balance-scale'
dataformat = 'csv' #spmf, csv
unions = set()
with open(filename + '.txt') as openfileobject:
    for line in openfileobject:
        if dataformat=='spmf':
            itemset = lineToItemset(line)
        elif dataformat=='csv':
            itemset = csvToItemset(line,index)
        #print(itemset)
        unions = unions.union(itemset)
        dataset.append(itemset)
        sizeOfPowerSet = math.pow(2,len(itemset))
        weights.append((index,sizeOfPowerSet))
        totalWeight += sizeOfPowerSet
        index += 1
    #print('union',unions)
    print('distinct item',len(unions))
        
print('finish reading')
fOut = open('outputItemset_' + filename + '.txt', 'w')
avgSupport = 0
for r in range(0,10000):
    chosenIndex = weightedChoice(weights,totalWeight)
    chosenItemset = dataset[chosenIndex]
    R = selectRandomSubset(chosenItemset)
    
    supportOfSelected = supportCalculator(R)
    avgSupport += supportOfSelected
    fOut.write('sup ' + str(supportOfSelected) + ' : ' + str(R) + '\n')
avgSupport /= 10000
print('average support ',avgSupport)
finishTime = time.time()
print('time elapsed',finishTime-startTime)