'''
Created on 25 Jan 2017

@author: user
'''
import itertools
import math
import random
import time

startTime = time.time()

def findsubsets(S):
    returnSet = list()
    for i in range(1,len(S)+1):
        resultTuple = itertools.combinations(S,i)
        for t in resultTuple:
            returnSet.append(set(t))
    return returnSet

def stringToSet(strInput):
    returnSet = set()
    splitResult = strInput.split(' ')
    for subStr in splitResult:
        if len(subStr):
            returnSet.add(subStr)
    return returnSet

def setToString(setInput):
    returnStr = ''
    for element in setInput:
        returnStr = returnStr + element + ' '
    return returnStr


def lineToSeq(lineInput):
    returnSeq = list()
    itemset = set()
    splitResult = lineInput.split(' ')
    for subStr in splitResult:
        if subStr=='-1':
            returnSeq.append(itemset)
            itemset = set()
        elif subStr=='-2\n':
            return returnSeq
        else:
            itemset.add(subStr)
    return returnSeq

def weightedChoice(choices,total):
    #total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    #print('random number :',r)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w


dataset = list()
weights = list()

maxLen = 0
with open('small.txt') as openfileobject:
    for line in openfileobject:
        seq = lineToSeq(line)
        if(len(seq) <= 50):
            dataset.append(seq)
            if(len(seq)>maxLen):
                maxLen = len(seq)

totalWeight = 0
index = 0


distinctSubs = list()
distinctSubs.append(list())

chosenIndex = 6
chosenSequence = dataset[chosenIndex]
print('chosen :',chosenSequence)
tempSet = list()
index = 0
for itemset in chosenSequence:
    print('itemset',index,',',len(distinctSubs),'distinctSubs')
    tempSet.clear()
    subsets = findsubsets(itemset)
    for existingSeq in distinctSubs:
        for subset in subsets:
            if len(existingSeq) == 0:
                newSeq = [subset]
            else:
                newSeq = list(existingSeq)
                newSeq.append(subset)
            if newSeq not in distinctSubs:
                tempSet.append(newSeq)
    distinctSubs.extend(tempSet)
    index += 1
print('elapsed time subseq generation',time.time()-startTime)
print(len(distinctSubs),'distinct subseq :',distinctSubs)
#print('elapsed time printing ',time.time()-startTime)

countItemset = [0] * len(chosenSequence)
c=0
for items in chosenSequence:
    for dif in distinctSubs:
        for itemsetDif in dif:
            inter = items.intersection(itemsetDif)
            if len(inter)>0:
                countItemset [c] += 1
                break
    c += 1
print(countItemset)  
