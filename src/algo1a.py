'''
Created on 1 Feb 2017

@author: user
'''

import itertools
import math
import random
import time
from _operator import itemgetter


startTime = time.time()
Lss = list()
dataTranspose = dict()
dataset = list() #list of list of set
weights = list()
phi = list()

def randomSubset(itemsetInput):
    subset = set()
    for item in itemsetInput:
        r = random.getrandbits(1)
        if r:
            subset.add(item)
    return subset

def findsubsets(S):
    returnSet = list()
    for i in range(1,len(S)+1):
        resultTuple = itertools.combinations(S,i)
        for t in resultTuple:
            returnSet.append(set(t))
    return returnSet

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

def supportCalculatorLong(dataset,subseq):
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

def generate_L(end_seq,S,item_n,position_set):
    interList = list()
    for h in range(end_seq,-1,-1):
        inter = item_n.intersection(S[h])
        if len(inter)>0:
            masuk = 1;
            for il in interList:
                if il.issuperset(inter):
                    masuk = 0
                    break
            if masuk == 1:
                interList.append(set(inter))
                position_set.append(h+1)
    
    return interList

def inclusion_exclusion_all_sub_sequence(position,level,temp,L,L_position,d):
    x = 0
    if level==0:
        x = (2**len(temp) - 1) * d[L_position[position]-1]
    else:
        for j in range(position-1,-1,-1):
            temp1 = L[j]
            temp1 = temp1.intersection(temp)
            if len(temp1) != 0:
                level -= 1
                x += inclusion_exclusion_all_sub_sequence(j,level,temp1,L,L_position,d)
                level += 1
    return x


def countDistinctSubseq(seq_list): # input type = list of set
    if len(seq_list)==0:
        return 1;
    seq_length = len(seq_list)
    d = list()
    d.append(1)
    for k in range(1,seq_length+1):
        d.append(0)
    Ls = list()
    for i in range(0,seq_length):
        L = list()
        L_position = list()
        item_n = seq_list[i]
        L=generate_L(i-1, seq_list,item_n,L_position)
        #print('L',L)
        #print('L_position',L_position)
        LRev = list(reversed(L))
        L_positionRev = list(reversed(L_position))
        if i>0:
            Ls.append(set(L_position))
        d[i+1] = (2**len(item_n)) * d[i]
        item_remove = 0
        one = -1
        temp_one = 1
        R = 0
        for level in range(0,len(L)):
            for j in range(len(L)-1,-1,-1):
                item = LRev[j]
                item_remove += inclusion_exclusion_all_sub_sequence(j, level, item, LRev, L_positionRev, d)
            d[i+1] += item_remove * one
            R += item_remove * temp_one
            item_remove = 0
            one = one * -1
            temp_one = temp_one * -1
    Lss.append(list(Ls))
    return d[len(d)-1]

def weightedChoice(choices,total):
    r = random.uniform(0, total)
    #print('random number :',r)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w

def setToSpmf(sequenceSet):
    spmf = ''
    for writeItemset in sequenceSet:
        for writeItem in writeItemset:
            spmf += writeItem + ' '
        spmf += '-1 '
    spmf += '-2'
    return spmf

maxDistinct = 0
totalWeight = 0
numberOfDistinctSubs = 0
index = 0
filename = 'synthetic1'
desiredSamples = 5000
with open(filename + '.txt') as openfileobject:
    for line in openfileobject:
        seq = lineToSeq(line,index)
        dataset.append(seq)
        numberOfDistinctSubs = countDistinctSubseq(seq)
        #print(numberOfDistinctSubs)
        phi.append(numberOfDistinctSubs)
        weights.append((index,numberOfDistinctSubs))
        totalWeight += numberOfDistinctSubs
        index += 1
orderedWeight = sorted(weights, key=itemgetter(1), reverse=True)
print('time read file',time.time()-startTime)
print(len(dataTranspose),'distinct items')
avgSupport = 0
fOut = open('sampling_' + filename + '.txt', 'w')
samplingTime = 0
supportTime = 0
writingTime = 0
r = 1
minsup = len(dataset)/10
print('minsup = ' + str(minsup) + ' sequences')
countFrequent = 0
while True:
    #if r%500 == 0 :
    #    print('checkpoint',r)
    startSampling = time.time()
    chosenIndex = weightedChoice(orderedWeight,totalWeight)
    chosenSequence = dataset[chosenIndex]
    #print('chosen :',chosenIndex,'.',chosenSequence)
    #print('Lss',Lss[chosenIndex])
    uGenerated = list()
    tempSet = list()
    index = 1
    p = 1
    for itemset in chosenSequence:
        #print('======i',index)
        #print('p',p)
        #allsubs = findsubsets(itemset)
        #allsubs.append(set())
        if index==p:
            #print('p == index')
            #selectedItemset = random.choice(allsubs)
            selectedItemset = randomSubset(itemset)
            #print('directly accept',selectedItemset)
            if len(selectedItemset) > 0:
                p = index+1
                uGenerated.append(set(selectedItemset))
        else:
            #print('p != index')
            while True:
                #selectedItemset = random.choice(allsubs)
                selectedItemset = randomSubset(itemset)
                #print('try',selectedItemset)
                flag = True
                if len(selectedItemset) == 0:
                    #print('accept',selectedItemset)
                    break 
                for xj in range(p,index):
                    if xj in Lss[chosenIndex][index-2]:
                        #print('check with index',xj)
                        if len(selectedItemset.difference(chosenSequence[xj-1])) == 0:
                            #print('reject',selectedItemset)
                            #allsubs.remove(selectedItemset)
                            flag = False
                            break
                if flag:
                    #print('accept',selectedItemset)
                    uGenerated.append(set(selectedItemset))
                    p = index+1
                    break
        index += 1
    endSampling = time.time()
    samplingTime += endSampling - startSampling
    supportOfSelected = supportCalculator(uGenerated)
    #avgSupport += supportOfSelected
    endSupport = time.time()
    supportTime += endSupport - endSampling
    if supportOfSelected > 1:
        print('sup ' + str(supportOfSelected) + ' : ' + setToSpmf(uGenerated))
    if supportOfSelected >= minsup and len(uGenerated) > 0:
        fOut.write('sup ' + str(supportOfSelected) + ' : ' + setToSpmf(uGenerated) + '\n')
        endWriting = time.time()
        writingTime += endWriting - endSupport
        countFrequent += 1
        print('sup ' + str(supportOfSelected) + ' : ' + setToSpmf(uGenerated))
        print(countFrequent)
    if r == 10000:
        print(str(countFrequent) + ' frequent sequences in 10K samples')
    if countFrequent == desiredSamples:
        break
    r += 1
#avgSupport /= 10000
print('average support',avgSupport)
finishTime = time.time()
print('time for sampling',samplingTime)
print('time for calculating support',supportTime)
print('time for writing file',writingTime)
print('time total',finishTime-startTime)