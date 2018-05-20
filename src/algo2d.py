'''
Created on 9 Jun 2017

@author: user
'''
import time
import random
from _operator import itemgetter

startTime = time.time()
dataTranspose = dict()
itemCount = list()
dataset = list() #list of list of set
weightsByItem = list()
distinctSubs = list()

def nCr(n,r):
    if r==0:
        return 1
    num = n
    for i in range(n-1,n-r,-1):
        num *= i
    denom = r
    for i in range(r-1,1,-1):
        denom *= i
    return num//denom

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

def inclusion_exclusion_all_sub_sequence(position,level,temp,L,L_position,d,one,nItem,i,n):
    comb = [nCr(len(temp),x) for x in range(0,len(temp)+1)]
    x = 0
    if level==0:
        x = (2**len(temp) - 1) * d[L_position[position]]
        for k3 in range(0,n+1):
            if nItem[L_position[position]][k3] == 0:
                break
            for k4 in range(1,len(temp)+1):
                nItem[i+1][k3+k4] += nItem[L_position[position]][k3] * comb[k4] * one
    else:
        for j in range(position-1,-1,-1):
            temp1 = L[j].intersection(temp)
            if len(temp1) != 0:
                level -= 1
                x += inclusion_exclusion_all_sub_sequence(j,level,temp1,L,L_position,d,one,nItem,i,n)
                level += 1
    return x

def calculateArea(seq_list,index): # input type = list of set
    if len(seq_list)==0:
        return 1;
    seq_length = len(seq_list)
    totalItems = 0
    for k in range(0,seq_length):
        totalItems += len(seq_list[k])
    d = list()
    d.append(1)
    t = list()
    for k in range(1,seq_length+1):
        d.append(0)
    for k2 in range(0,totalItems+1):
        t.append(0)
    nItem = list()
    for k in range(0,seq_length+1):
        nItem.append(list(t))
    nItem[0][0] = 1
    for i in range(0,seq_length):
        L = list()
        L_position = list()
        item_n = set(seq_list[i])
        combinationList = [nCr(len(item_n),x) for x in range(0,len(item_n)+1)]
        for k3 in range(0,totalItems+1):
            if nItem[i][k3] == 0:
                break
            for k4 in range(1,len(item_n)+1):
                nItem[i+1][k3+k4] += nItem[i][k3] * combinationList[k4] 
        for k3 in range(0,totalItems+1):
            nItem[i+1][k3] += nItem[i][k3]
        L=generate_L(i-1, seq_list,item_n,L_position)
        d[i+1] = (2**len(item_n)) * d[i]
        item_remove = 0
        one = -1
        temp_one = 1
        R = 0
        for level in range(0,len(L)):
            for j in range(len(L)-1,-1,-1):
                item = set(L[j])
                item_remove += inclusion_exclusion_all_sub_sequence(j, level, item, L, L_position, d, one, nItem,i,totalItems)
            d[i+1] += item_remove * one
            R += item_remove * temp_one
            item_remove = 0
            one = one * -1
            temp_one = temp_one * -1
    #for k in range(0,seq_length+1):
        #print(nItem[k])
    itemCount.append(list(nItem[seq_length]))
    #print(d[len(d)-1])
    return d[len(d)-1]

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
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    return c

def chooseSize(choices,total):
    r = random.uniform(0, total)
    upto = 0
    size = 0
    for amount in choices:
        if upto + amount >= r:
            return size
        upto += amount
        size += 1
    return size

def chooseSubseq(seq,size):
    subseq = list()
    totalItems = 0
    for k in range(0,len(seq)):
        totalItems += len(seq[k])
    indices = [x for x in range(0,totalItems)]
    randomIndices = random.sample(indices,size)
    currentItemset = 0
    separator = len(seq[currentItemset])
    n = 0
    for pos in range(0,totalItems):
        if pos >= separator:
            if n > 0:
                subseq.append(set(random.sample(seq[currentItemset],n)))
            n = 0
            currentItemset += 1
            separator += len(seq[currentItemset])
        if pos in randomIndices:
            n += 1
    if n>0:
        subseq.append(set(random.sample(seq[currentItemset],n)))
    return subseq
    
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

totalWeightItem = 0
index = 0
filename = 'SIGN.txt'
desiredSamples = 10000
with open(filename) as openfileobject:
    for line in openfileobject:
        #if index==4:
        seq = lineToSeq(line,index)
        dataset.append(seq)
        distinctSubs.append(calculateArea(seq, index))
        area = 0
        for i in range(1,len(itemCount[index])):
            area += i * itemCount[index][i]
        weightsByItem.append((index,area))
        totalWeightItem += area
        index += 1
        
orderedWeight = sorted(weightsByItem, key=itemgetter(1), reverse=True)
avgSupport = 0
fOut = open('samplingAreaItem_' + filename, 'w')
for i in range(0,desiredSamples):
    chosenIndex = weightedChoice(orderedWeight, totalWeightItem)
    chosenSequence = dataset[chosenIndex]
    chosenSize = chooseSize(itemCount[chosenIndex], distinctSubs[chosenIndex])
    chosenSubsequence = chooseSubseq(chosenSequence, chosenSize)
    support = supportCalculator(chosenSubsequence)
    avgSupport += support
    fOut.write(str(support) + ' ' + str(chosenSubsequence) + '\n')
fOut.close()
finishTime = time.time()
avgSupport = avgSupport / desiredSamples
print('total runtime',finishTime-startTime)
print('average support',avgSupport)