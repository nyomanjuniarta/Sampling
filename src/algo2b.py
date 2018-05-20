'''
Created on 8 Jun 2017

@author: user
'''
import itertools
import random
from _operator import itemgetter

dataTranspose = dict()
dataset = list() #list of list of set
weightsByItemset = list()
weightsByItem = list()

def findSubsets(S):
    returnSet = list()
    for i in range(1,len(S)+1):
        resultTuple = itertools.combinations(S,i)
        for t in resultTuple:
            returnSet.append(set(t))
    return returnSet

def setToSpmf(itemset):
    spmf = ''
    for item in itemset:
        spmf += item + ' '
    spmf += '-1'
    return spmf

def generateADS(seq,f):
    allSubseq = set() # set of subsequences (spmf)
    allSubseq.add('')
    for itemset in seq:
        allSubset = findSubsets(itemset)
        if f==1:
            print('itemset',itemset)
            print('allSubset',allSubset)
        allSubseqPrev = set(allSubseq)
        for existingSubseq in allSubseqPrev:
            for subset in allSubset:
                if f==1:
                    print(existingSubseq + ' ' + setToSpmf(subset))
                allSubseq.add(existingSubseq + ' ' + setToSpmf(subset))
    return allSubseq

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

def calculateArea(allSubseq):
    areaByItemset = 0
    areaByItem = 0
    for subseq in allSubseq:
        items = subseq.split(' ')
        itemsetCount = items.count('-1')
        areaByItemset += itemsetCount
        areaByItem += len(items) - itemsetCount - 1
    return (areaByItemset,areaByItem)

def weightedChoice(choices,total):
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    return c

totalWeightItemset = 0
totalWeightItem = 0
index = 0
filename = 'synthetic8.txt'
desiredSamples = 10
with open(filename) as openfileobject:
    for line in openfileobject:
        seq = lineToSeq(line,index)
        dataset.append(seq)
        allSubseq = generateADS(seq,0)
        area = calculateArea(allSubseq)
        areaByItemset = area[0]
        areaByItems = area[1]
        weightsByItemset.append((index,areaByItemset))
        weightsByItem.append((index,areaByItems))
        totalWeightItemset += areaByItemset
        totalWeightItem += areaByItems
        index += 1

orderedWeightItemset = sorted(weightsByItemset, key=itemgetter(1), reverse=True)
orderedWeightItem = sorted(weightsByItem, key=itemgetter(1), reverse=True)

'''for i in range(0,desiredSamples):
    chosenIndex = weightedChoice(orderedWeightItemset, totalWeightItemset)
    chosenSequence = dataset[chosenIndex]
    print('chosen ',chosenSequence)'''
    