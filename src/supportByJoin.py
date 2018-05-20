'''
Created on 22 Jun 2017

@author: user
'''

dataTranspose = dict()
dataset = list() #list of list of set

def temporalJoin(tuplesA, tuplesB):
    joined = list()
    for tA in tuplesA:
        for tB in tuplesB:
            0
    return joined

def equalityJoin(tuplesA, tuplesB):
    joined = list()
    return joined

def supportByJoin(subseq):
    return 0

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
                dataTranspose[subStr] = {(lineNum,itemsetNum)}
            else:
                dataTranspose[subStr].add((lineNum,itemsetNum))
    return returnSeq

index = 0
datasetFile = 'small.txt'
toBeCalculated = 'smallCalc.txt'
with open(datasetFile) as openfileobject:
    for line in openfileobject:
        seq = lineToSeq(line,index)
        dataset.append(seq)
        index += 1

for keys in dataTranspose.keys():       
    a = list(dataTranspose[keys])
    a.sort()
    print(keys,a)

'''fOut = open('output_' + toBeCalculated, 'w')
with open(toBeCalculated) as openfileobject:
    for line in openfileobject:
        returnSeq = list()
        itemset = set()
        splitResult = line.split(' ')
        itemsetNum = 0
        for subStr in splitResult:
            if subStr=='-1':
                returnSeq.append(itemset)
                itemset = set()
                itemsetNum += 1
            else:
                itemset.add(subStr)
        #fOut.write('SUP = ' + str(supportCalculator(returnSeq)) + ' : ' + line)
        fOut.write('SUP = ' + str(supportCalculatorLong(returnSeq)) + ' : ' + line)'''