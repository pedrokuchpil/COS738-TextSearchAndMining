import os
import re
from xml.etree import ElementTree as ET

class Query:
    def __init__(self, q):
        self.number = q.find('QueryNumber').text
        self.text = re.sub("[^a-zA-Z] ", " ", q.find('QueryText').text).upper().replace('\n', '')
        self.text = ' '.join(self.text.split())
        self.results = q.find('Results').text
        self.records = {}
        for i in q.iter('Item'):
                self.records[i.text] = i.get('score')

class QueryProcessor:
    def __init__(self, file):
        self.query_object_list = []
        self.leia_path = ''
        self.consultas_path = ''
        self.esperados_path = ''
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if ('LEIA' in line):
                    self.leia_path = line.partition('=')[2].rstrip()
                    doc = ET.parse(self.leia_path).getroot()
                    for q in doc.findall('QUERY'):
                        self.query_object_list.append(Query(q))
                elif ('CONSULTAS' in line):
                    self.consultas_path = line.partition('=')[2].rstrip()
                elif ('ESPERADOS' in line):
                    self.esperados_path = line.partition('=')[2].rstrip()
                
                        
    def generate_consultas(self):
        with open(self.consultas_path, 'w', encoding='utf-8') as f:
            f.write('QueryNumber;QueryText\n')
            for item in self.query_object_list:
                f.write(item.number + ';' + item.text + '\n')
    
    
    
    def generate_esperados(self):
        
        def sum_votes(votes):
            sum = 0
            for v in votes:
                if v != '0':
                    sum += 1
            return str(sum)

        with open(self.esperados_path, 'w', encoding='utf-8') as f:
            f.write('QueryNumber;DocNumber;DocVotes\n')
            for q in self.query_object_list:
                for document, votes in q.records.items():
                    f.write(q.number + ';' + document + ';' + sum_votes(votes) + '\n')
