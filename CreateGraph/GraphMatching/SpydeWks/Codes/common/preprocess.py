import csv
import nltk
import numpy as np
import unicodedata
import time
import random

from nltk.tokenize import RegexpTokenizer
from math import sqrt
import re
from itertools import islice
from blist import blist
#from nltk.stem.porter import PorterStemmer
#stemmer = PorterStemmer()
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

from nltk.util import ngrams

#field pairs values
class fieldPairSim:                       
    def __init__(self, fieldA, fieldB, value ):
        self.fieldA = fieldA
        self.fieldB = fieldB
        self.value = value
        
        
class TbfieldValue:
    def __init__(self, tableA, fieldA, value ):
        self.tableA = tableA
        self.fieldA = fieldA
        self.value = value
        
        
class preprocess(object):

    def __init__(self):
        pass

    #lowercase every item in a list
    def word_strip_lower(self, tokens):
        return [str(tkn).lower().replace('\n', '').replace('\\N', '').replace('\t', ' ').strip() for tkn in tokens]
      
    #filter '\n', '\na' value
    def filterNullValueLst(self, valList):
        valList = self.word_strip_lower(valList)
        newList = blist([])
        for v in valList:
            if v != '\\n' and v != '\\na' and v != '\n' and v != '\na' and v != 'nan' and v != '\nan' and v != '\\nan' and v != '':
                #print (v)
                newList.append(v)
        return newList


    def filterNullValueAndLowercaseLst(self, valSet):
        newList = blist([])
        for v in valSet:
            #print (v)
            v = str(v).lower().replace('\n', '').replace('\\N', '').replace('\t', ' ').strip()
            #print (v)
            if v != '\\n' and v != '\\na' and v != '\n' and v != '\na' and v != 'nan' and v != '\nan' and v != '\\nan' and v != '' and v != '' and v != ' ' and v != '-' and v != '_':
                newList.append(v)
            #print (v)

        return newList


    def filterNullValueAndLowercaseSet(self, valSet):
        newSet = set()
        for v in valSet:
            v = str(v).lower().replace('\\N', '\n').replace('\n', '').replace('\t', ' ').strip()
            if v != '\\n' and v != '\\na' and v != '\n' and v != '\na' and v != 'nan' and v != '\nan' and v != '\\nan' and v != '' and v != '' and v != ' ' and v != '-' and v != '_':
                #print (v)
                newSet.add(v)
        return newSet
        
    #filter '\n', '\na' value
    def filterNullValueForPrimaryKey(self, valList):
        valList = self.word_strip_lower(valList)
        newList = blist([])
        for v in valList:
            if v != '\\n' and v != '\\na' and v != '\n' and v != '\na' and v != 'nan' and v != '\nan' and v != '\\nan' and v != '' and v != '' and v != ' ' and v != '-' and v != '_':
                #print (v)
                newList.append(v)
        return newList

    #text = "I am aware that nltk only offers bigrams and trigrams"
    def getNgrams(self, text, n):
        tokens = nltk.word_tokenize(text)
        ngram_out = ngrams(tokens, n)
        return ngram_out

    def judgeListAllNonNumerical(self, listIn):
        if len(listIn) == 0:
            return False
        count = 0
        for ele in listIn:
            if self.is_number(ele) is False:
                count += 1
                if (count >= 0.6667*len(listIn)):                  #
                    return True
        return False

    # decide the list are all numbers,  list element are string type , statistic ordinal number's count, if half of them are ordina,
    # we think it's ordinal numbers
    def judgeListAllNumbers(self, listIn):
        if len(listIn) == 0:
            return False
        count = 0
        for ele in listIn:
            if self.is_number(ele) is True:
                count += 1
                if (count >= 0.6667*len(listIn)):            #50% are numers, we assume the list is numerical
                    return True
        return False

    #infer one string is number  # negative, float, integer are all numbers
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

     #split big dictionary into small dictionary for multithread
    def splitDictchunks(self, dictMap, size):
        it = iter(dictMap)
        for i in range(0, len(dictMap), size):
            yield {k:dictMap[k] for k in islice(it, size)}


    # example:  DESKTOP/IBM/VIP, OC-48/STM-16,  Chnl-Pass, cisco3850=>cisco 3850
    def parseToken(self, singleToken):
       # r = re.compile("([a-zA-Z]+)([0-9]+)")
        return set(filter(None, re.split(r'(\d+)', singleToken)))

    
    def stem_tokens(self, tokens, stemmer):
        stemmed = blist([])
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed
 

    def tokenizeStem(self,text):
        tokens = nltk.word_tokenize(text)
        stems = self.stem_tokens(tokens, stemmer)
        return stems
    
    def stemOneToken(self, token):
        stem = stemmer.stem(token)
        return stem


    '''
    # preprocess one record, tokenize, parse, stem
    def parseStemOneRecord(self, recordStr, prefixlLength):
        #newSet = set([str(recordStr).lower().replace('\\N', '\n').replace('\n', '').replace('\t', ' ').replace('/', ' ').replace('-', ' ').replace('=', ' ').replace('.', ' ').replace('\'', ' ').replace('_', ' ').replace('@', ' ').strip()])
        newSet = str(recordStr).lower().replace('\\N', '\n').replace('\n', '').replace('\t', ' ').strip()
        #print ('recordStr', newSet)
        resultSet = set()
        #for recd in [newSet]:
            #if (not re.match(r'^[\d]*$', recd)) and (not re.match(r'[a-zA-Z]*$', newSet)):              #not digit or alphabetic only
        if not newSet.isdigit():                            #not digit only
            tokenizer = RegexpTokenizer(r'\w+')              #word only, remove everything else
            parsedOutSet = set(tokenizer.tokenize(newSet))       #tokenize
           # print ('parsedOutSet1111:', parsedOutSet)
            for out in parsedOutSet:
                #parsedOutSet = parsedOutSet | set(self.parseToken(out))             # parse split nexus121
                parsedOutSet = set(self.parseToken(out))
          #  print ('parsedOutSet', parsedOutSet)
            for parOut in set(parsedOutSet):
                if parOut.isdigit():
                    resultSet.add(parOut)                    #need to contain original splitted ones?
                    tmp = ''
                    for i in range(len(parOut)-prefixlLength):      #separate
                        tmp += 'x'
                    newStr = parOut[:prefixlLength] + tmp
                    resultSet.add(newStr)
                else:
                    resultSet.add(parOut)
                    resultSet.add(self.stemOneToken(parOut)) 
         #   print ('xxxx  ', newSet)
        else:
            newStr = newSet[:prefixlLength]
            tmp = ''
            for i in range(len(newSet)-prefixlLength):      #separate
                tmp += 'x'
            newStr = newSet[:prefixlLength] + tmp
            resultSet.add(newStr)
            #print ('len(newStr)', newStr)
        return resultSet
    '''

    # preprocess one record, tokenize, parse, stem
    def parseStemOneRecord(self, recordStr, prefixlLength):
        #newSet = set([str(recordStr).lower().replace('\\N', '\n').replace('\n', '').replace('\t', ' ').replace('/', ' ').replace('-', ' ').replace('=', ' ').replace('.', ' ').replace('\'', ' ').replace('_', ' ').replace('@', ' ').strip()])
        newSet = str(recordStr).lower().replace('\\N', '\n').replace('\n', '').replace('\t', ' ').strip()
        #print ('recordStr', recordStr, newSet)
        resultSet = set()
        for recd in [newSet]:
            #if (not re.match(r'^[\d]*$', recd)) and (not re.match(r'[a-zA-Z]*$', newSet)):              #not digit or alphabetic only
            if not recd.isdigit():                            #not digit only
                tokenizer = RegexpTokenizer(r'\w+')              #word only, remove everything else
                parsedOutSet = set(tokenizer.tokenize(recd))       #tokenize
               # print ('parsedOutSet1111:', parsedOutSet)
                for out in parsedOutSet:
                    parsedOutSet = parsedOutSet | set(self.parseToken(out))             # parse split nexus121
                    #parsedOutSet = set(self.parseToken(out))
                #print ('parsedOutSet', parsedOutSet)
                for parOut in set(parsedOutSet):
                    if parOut.isdigit():
                       # resultSet.add(parOut)         #need to contain original splitted ones?
                        tmp = ''
                        for i in range(len(parOut)-prefixlLength):      #separate
                            tmp += 'x'
                        newStr = parOut[:prefixlLength] + tmp
                        resultSet.add(newStr)
                    else:
                        resultSet.add(parOut)
                        resultSet.add(self.stemOneToken(parOut)) 

             #   print ('xxxx  ', newSet)
            else:
                newStr = recd[:prefixlLength]
                tmp = ''
                for i in range(len(recd)-prefixlLength):      #separate
                    tmp += 'x'
                newStr = recd[:prefixlLength] + tmp
                resultSet.add(newStr)
                #print ('len(newStr)', newStr)
        return resultSet



    #input setA, setB, output the cosine similarity
    def cosSimilarity(self, setA, setB):
        cosRes = 0
        if (len(setA) == 0 or len(setB) == 0):
            return cosRes
        
        commonSetLen = len(set(setA & setB))
        #print ('commonSetLen ', commonSetLen) 
        if (commonSetLen == 0):
            return cosRes

        ABMagn = sqrt(len(setA)*len(setB))
        
        cosRes = commonSetLen/ABMagn

        return cosRes

    def generateRandomIndex(self, maxlenColumns, numberGen):
        lstRange =range(0, maxlenColumns)
        lstIndex = random.sample(lstRange, numberGen)

        return lstIndex

    
def main():
    preproc = preprocess()
    totalStart = time.time()
    inputPairs = (('c2950', 'c2956'), ('csco900 series', 'csco series'), ('cisco8 series', 'cisco800 series'), ('cs2950', 'cs2916'), ('c800', 's800'), ('ts900', 'cs900'))
    for pr in inputPairs:        #[3:4]:
        setA = preproc.parseStemOneRecord(pr[0], 2)
        setB = preproc.parseStemOneRecord(pr[1], 2)
        c = preproc.cosSimilarity(setA, setB)
       # print ('setA B: ', setA, setB)
        print ('(' + pr[0] + ',' + pr[1] + ')' +'  NEMA similarity: ', c)
        
    totalEnd = time.time()
    print ('total time', totalEnd - totalStart)

  #  cosR = preproc.cosSimilarity(preproc.parseStemOneRecord('mem4761 products', 1), preproc.parseStemOneRecord('mem-4700m-64d=', 1))
  #  print ('vecA, vecB ', cosR)
    '''
   # ls = ['nexs333dddd4444','DDDDD/TTT', 'production tta']
    lsA = ['products', 'cisco', '9100','mem-4700m-64d=','444-335', 'nexus9102']
    lsB = ['prod', 'nexus9102']

   # print (preproc.parseToken(lsA[0]))

   # print (blist(preproc.tokenizeStem(psa) for psa in lsB))
    print (preproc.parseStemLst(lsA,2))
    print (preproc.parseStemLst(lsB,2))

    if (not re.match(r'^[\d]*$', '34444')):
        
        print ('xxxxxx')
   
    if (not re.match(r'[a-zA-Z]*$', 'tttt')):
        
        print ('ttttttt')

    cosR = preproc.cosSimilarity(preproc.parseStemLst(lsA,2), preproc.parseStemLst(lsB,2))
    print ('vecA, vecB ', cosR)
    '''

if __name__ == "__main__":
    main()




