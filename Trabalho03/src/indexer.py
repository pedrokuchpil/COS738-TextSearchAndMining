from operator import invert
import os
import re

class Indexer():
    def __init__(self, file):
        self.leia_path = ''
        self.escreva_path = ''
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if ('LEIA' in line):
                    self.leia_path = line.partition('=')[2].rstrip()
                elif ('ESCREVA' in line):
                    self.escreva_path = line.partition('=')[2].rstrip()

    def generate_tf(self):
        with open(self.leia_path, 'r', encoding='utf-8') as inverted:
            next(inverted)
            inverted_list = {}
            for line in inverted:
                word = re.sub('[^A-Z]', '', line.partition(';')[0].rstrip().upper())
                docs = line.rstrip('\n').partition(';')[2].lstrip('[').rstrip(']').split(',')
                if (len(word) > 2):
                    inverted_list[word] = docs
                
        tf = {}
        for key, value in inverted_list.items():
            for doc in value:
                if (doc not in tf):
                    tf[doc] = {}
                elif key not in tf[doc]:
                    tf[doc][key] = 1
                else:
                    tf[doc][key] += 1
        return tf

    #def generate_itf(tf):
        
