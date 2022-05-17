from operator import invert
import os
import re
import math
import json

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

    def tf_idf(self):
        self.generate_tf()
        self.generate_idf()
        tf_idf = {}
        for doc, words in self.tf.items():
            for word in words:
                if doc not in tf_idf:
                    tf_idf[doc] = {}
                try:
                    tf_idf[doc][word] = self.tf[doc][word] * self.idf[word]
                except:
                    tf_idf[doc][word] = 0

        return tf_idf

    def to_json(self):
        tf_idf = self.tf_idf()
        with open(self.__escreva_path, 'w', encoding='utf-8') as f:
            json.dump(tf_idf, f)
        
    