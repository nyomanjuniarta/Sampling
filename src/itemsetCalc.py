'''
Created on 2 Mar 2017

@author: user
'''
from statistics import mean

itemsetCount = list()
itemPerItemsetCount = list()
itemPerSeqCount = list()

filename = 'FIFA'
countIt = 0
countSet = 0
countItTot = 0
with open(filename + '.txt') as openfileobject:
    for line in openfileobject:
        splitResult = line.split(' ')
        for subStr in splitResult:
            if subStr=='-1':
                countSet += 1
                countItTot += countIt
                itemPerItemsetCount.append(countIt)
                countIt = 0
            elif subStr=='-2\n':
                itemsetCount.append(countSet)
                countSet = 0
                itemPerSeqCount.append(countItTot)
                countItTot = 0
            else:
                countIt += 1


print('avg itemset per seq',mean(itemsetCount))
print('avg item per itemset',mean(itemPerItemsetCount))
print('avg item per seq',mean(itemPerSeqCount))