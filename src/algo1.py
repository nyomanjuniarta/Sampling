'''
Created on 16 Jan 2017

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
with open('BMS2.txt') as openfileobject:
    for line in openfileobject:
        seq = lineToSeq(line)
        dataset.append(seq)
        if(len(seq)>maxLen):
            maxLen = len(seq)
print('maxlen',maxLen)
totalWeight = 0
index = 0
for data in dataset:
    weight = math.pow(2,len(data)-maxLen+1)
    weights.append((index,weight))
    totalWeight += weight
    index += 1
print('elapsed time read file',time.time()-startTime)

'''print('example of weighted random')
#sampleCount = [0]*len(dataset)
for i in range(1,100):
    #print(random.uniform(0, 100))
    s = weightedChoice(weights,totalWeight)
    #sampleCount[s] += 1
    print('sequence',weights[s][0],'length',len(dataset[s]),':',dataset[s])
#print(sampleCount)'''

distinctSubs = list()
distinctSubs.append(list())

subi = time.time()
chosenIndex = weightedChoice(weights,totalWeight)
#chosenIndex = 11
chosenSequence = dataset[chosenIndex]
print('chosen :',chosenIndex,'.',chosenSequence)
'''tempSet = list()
index = 0
for itemset in chosenSequence:
    #print('itemset',index,',',len(distinctSubs),'distinctSubs')
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
print('elapsed time subseq generation',time.time()-subi)
print(len(distinctSubs),'distinct subseq')
#print('elapsed time printing ',time.time()-startTime)'''

'''print('uniformly chosen subsequences :')
subsList = list(distinctSubs)
print('elapsed time sets to list',time.time()-startTime)
for i in range(1,10):
    print(random.choice(subsList))
print('elapsed time random uniform',time.time()-startTime)'''