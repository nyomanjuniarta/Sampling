'''
Created on 30 Mar 2017

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
                interList.append(inter)
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

def countDistinctSubseq(seq_list):  # input type = list of set
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
    Lss.append(Ls)
    return d[len(d)-1]

maxDistinct = 0
totalWeight = 0
numberOfDistinctSubs = 0
index = 0
filename = 'small'
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
print(Lss)