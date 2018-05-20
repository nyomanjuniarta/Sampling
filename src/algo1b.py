'''
Created on 1 Jun 2017

@author: user
coba kalau subsequence diberi weight
'''
import itertools
import math
import random
import time
from _operator import itemgetter


startTime = time.time()
dataTranspose = dict()
dataset = list() #list of list of set
weights = list()

def randomSubset(itemsetInput):
    subset = set()
    for item in itemsetInput:
        r = random.getrandbits(1)
        if r:
            subset.add(item)
    return subset

def findSubsetsAndWeight(S):
    returnSet = list()
    maxLen = len(S)
    for i in range(1,len(S)+1):
        resultTuple = itertools.combinations(S,i)
        for t in resultTuple:
            returnSet.append((set(t),maxLen-len(t)))
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
    L = list()
    for k in range(0,end_seq+1):
        intersection = item_n.intersection(S[k])
        if len(intersection) != 0:
            new_item = set(intersection)
            # begin addelement
            i = 0
            size = len(L)
            while i<size:
                if new_item.issuperset(L[i]):
                    del position_set[i]
                    del L[i]
                    size -= 1
                else:
                    i += 1
            L.append(set(new_item))
            position_set.append(k)
            # end addelement
    return L

def inclusion_exclusion_all_sub_sequence(position,level,temp,L,L_position,d):
    x = 0
    if level==0:
        x = (2**len(temp) - 1) * d[L_position[position]]
    else:
        for j in range(position-1,-1,-1):
            temp1 = L[j].intersection(temp)
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
    for i in range(0,seq_length):
        L = list()
        L_position = list()
        item_n = set(seq_list[i])
        L=generate_L(i-1, seq_list,item_n,L_position)
        d[i+1] = (2**len(item_n)) * d[i]
        item_remove = 0
        one = -1
        temp_one = 1
        R = 0
        for level in range(0,len(L)):
            for j in range(len(L)-1,-1,-1):
                item = set(L[j])
                item_remove += inclusion_exclusion_all_sub_sequence(j, level, item, L, L_position, d)
            d[i+1] += item_remove * one
            R += item_remove * temp_one
            item_remove = 0
            one = one * -1
            temp_one = temp_one * -1
    return d[len(d)-1]

def weightedChoice(choices,total):
    r = random.uniform(0, total)
    #print('random number :',r)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    return c

def setToSpmf(sequenceSet):
    spmf = ''
    for writeItemset in sequenceSet:
        for writeItem in writeItemset:
            spmf += writeItem + ' '
        spmf += '-1 '
    spmf += '-2'
    return spmf

def weightedSubsetSelection(itemset):
    totalWeight = len(itemset) * (2**(len(itemset)-1)) 
    emptyOrNot = random.randint(0,20)
    if emptyOrNot < 20:
        return set()
    subsetsAndWeight = list(findSubsetsAndWeight(itemset)) 
    chosenSubset = weightedChoice(subsetsAndWeight, totalWeight)
    return chosenSubset

totalWeight = 0
index = 0
filename = 'synthetic1.txt'
desiredSamples = 5000
with open(filename) as openfileobject:
    for line in openfileobject:
        seq = lineToSeq(line,index)
        dataset.append(seq)
        ads = countDistinctSubseq(seq)
        weights.append((index,ads))
        totalWeight += ads
        index += 1
orderedWeight = sorted(weights, key=itemgetter(1), reverse=True)

for i in range(0,desiredSamples):
    chosenIndex = weightedChoice(orderedWeight, totalWeight)
    chosenSequence = dataset[chosenIndex]
    print('chosen =',chosenSequence)
    sample = list()
    for itemset in chosenSequence:
        chosenSubset = weightedSubsetSelection(itemset)
        if(len(chosenSubset) > 0):
            sample.append(set(chosenSubset))
    print(supportCalculator(sample),sample)