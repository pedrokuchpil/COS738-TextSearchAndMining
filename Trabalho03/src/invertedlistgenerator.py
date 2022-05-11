import os
import re
from xml.etree import ElementTree as ET
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class Record:
    def __init__(self, r):
        self.recordnum = r.find('RECORDNUM').text.replace(' ','')
        try:
            self.abstract = r.find('ABSTRACT').text
        except AttributeError:
            try:
                self.abstract = r.find('EXTRACT').text
            except AttributeError:
                print('NÃO FOI POSSÍVEL ABRIR' + self.recordnum)
                self.abstract = ' '


class InvertedListGenerator:
    def __init__(self, file):
        self.record_object_list = []
        self.leia_path = []
        self.escreva_path = ''
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if ('LEIA' in line):
                    self.leia_path.append(line.partition('=')[2].rstrip())
                elif ('ESCREVA' in line):
                    self.escreva_path = line.partition('=')[2].rstrip()
        for file in self.leia_path:
            doc = ET.parse(file).getroot()
            for r in doc.findall('RECORD'):
                self.record_object_list.append(Record(r))
        
    def generate_escreva(self):
        stop_words = set(stopwords.words('english'))
        dict = {}
        for record in self.record_object_list:
            text = re.sub('[^a-zA-Z\s]', ' ', record.abstract.replace('\n', ' ')).upper()
            word_tokens = word_tokenize(text)
            filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words and len(w) > 2]

            for word in filtered_sentence:
                if (word not in dict):
                    dict[word] = []
                dict[word] = dict[word] + [record.recordnum]

        with open(self.escreva_path, 'w', encoding='utf-8') as f:
            f.write('Word;Documents\n')
            for key, value in dict.items():
                f.write(key + ';' + str(value) + '\n')
