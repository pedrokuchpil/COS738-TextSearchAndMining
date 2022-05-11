import os
import json
import re
import math

from indexer import invert_tf
from nltk.tokenize import word_tokenize

def generate_consultas(file):
        with open(file, 'r', encoding='utf-8') as f:
            queries = {}
            next(f)
            for line in f:
                querynumber = line.strip('\n').partition(';')[0]
                querytext = line.strip('\n').partition(';')[2]
                queries[querynumber] = querytext
        return queries

def create_tf_idf(file):
        queries = generate_consultas(file)
        inverted_list = {}

        for num, text in queries.items():
            text = re.sub('[^a-zA-Z\s]', ' ', text).replace('\n', ' ').upper()
            word_tokens = word_tokenize(text)

            for word in word_tokens:
                if (word not in inverted_list):
                    inverted_list[word] = []
                inverted_list[word] = inverted_list[word] + [num]

        tf = {}
        for word, documents in inverted_list.items():
            for doc in documents:
                if (doc not in tf):
                    tf[doc] = {}
                try:
                    tf[doc][word] += 1
                except:
                    tf[doc][word] = 1
        
        idf = {}
        itf = invert_tf(tf)
        for word in itf:
            idf[word] = math.log(len(tf)/len(itf[word]))
        
        tf_idf = {}
        for doc, words in tf.items():
            for word in words:
                if doc not in tf_idf:
                    tf_idf[doc] = {}
                try:
                    tf_idf[doc][word] = tf[doc][word] * idf[word]
                except:
                    tf_idf[doc][word] = 0
        return tf_idf

def cos_similarity(tf_idf1, tf_idf2):
    dot = 0
    for d1 in tf_idf1:
        for d2 in tf_idf2:
            if d1 == d2:
                dot += tf_idf1[d1]*tf_idf2[d2]
    magnitude = math.sqrt(sum([tf_idf1[t1]**2 for t1 in tf_idf1])) * math.sqrt(sum([tf_idf2[t2]**2 for t2 in tf_idf2]))
    try:
        return (dot/magnitude)
    except:
        return 0

class Searcher:

    def __init__(self, file):
            self.__modelo_path = ''
            self.__consultas_path = ''
            self.__resultados_path = ''
            self.model_tf_idf = {}
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    if ('MODELO' in line):
                        self.__modelo_path = line.partition('=')[2].rstrip()
                    elif ('CONSULTAS' in line):
                        self.__consultas_path = line.partition('=')[2].rstrip()
                    elif ('RESULTADOS' in line):
                        self.__resultados_path = line.partition('=')[2].rstrip()
            
            with open(self.__modelo_path, encoding='utf-8') as json_file:
                self.model_tf_idf = json.load(json_file)
    
    def run_searches(self):
        queries_tf_idf = create_tf_idf(self.__consultas_path)
        searches = {}
        for query in queries_tf_idf:
            for doc in self.model_tf_idf:
                if query not in searches:
                    searches[query] = {}
                if doc not in searches[query]:
                    searches[query][doc] = cos_similarity(queries_tf_idf[query], self.model_tf_idf[doc])
        
        for query, docs in searches.items():
            searches[query] = {k: v for k, v in sorted(docs.items(), key=lambda item: item[1], reverse = True)}
        #print(searches)
    
        with open(self.__resultados_path, 'w', encoding='utf-8') as f:
            f.write('QueryNumber;List\n')
            for query, docs in searches.items():
                cont = 1
                for doc in docs:
                    lista = [cont, doc, searches[query][doc]]
                    f.write(query + ';' + str(lista) + '\n')
                    cont += 1
