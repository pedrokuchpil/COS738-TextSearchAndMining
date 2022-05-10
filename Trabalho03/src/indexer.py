from operator import invert
import os
import re
import math

def invert_tf(tf):
    itf = {}
    for doc, words in tf.items():
        for word in words:
            if word not in itf:
                itf[word] = {}
            try:
                itf[word][doc] = tf[doc][word]
            except:
                itf[word][doc] = {}
    return itf

class Indexer():
    def __init__(self, file):
        self.__leia_path = ''
        self.__escreva_path = ''
        self.tf = {}
        self.idf = {}
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if ('LEIA' in line):
                    self.__leia_path = line.partition('=')[2].rstrip()
                elif ('ESCREVA' in line):
                    self.__escreva_path = line.partition('=')[2].rstrip()

    def generate_tf(self):
        with open(self.__leia_path, 'r', encoding='utf-8') as inverted:
            next(inverted)
            inverted_list = {}
            for line in inverted:
                word = re.sub('[^A-Z]', '', line.partition(';')[0].rstrip().upper())
                docs = re.sub('[^\d/g,]', '', line.partition(';')[2]).replace('\n', '').split(',')
                if (len(word) > 2):
                    inverted_list[word] = docs
                
        tf = {}
        for word, documents in inverted_list.items():
            for doc in documents:
                if (doc not in tf):
                    tf[doc] = {}
                try:
                    tf[doc][word] += 1
                except:
                    tf[doc][word] = 1
        self.tf = tf

    def generate_idf(self):
        idf = {}
        itf = invert_tf(self.tf)
        for word in itf:
            idf[word] = math.log(len(self.tf)/len(itf[word]))
        self.idf = idf        


        
