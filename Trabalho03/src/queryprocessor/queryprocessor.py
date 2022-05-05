import os
import re
from xml.etree import ElementTree as ET

class Query:
    def __init__(self, q):
        self.number = int(q.find('QueryNumber').text)
        self.text = re.sub("[^a-zA-Z] ", "", q.find('QueryText').text).replace('\n', ' ').upper()
        self.results = int(q.find('Results').text)
        self.records = {}
        for i in q.iter('Item'):
                self.records[i.text] = i.get('score')

class QueryProcessor:
    def __init__(self, file):
        self.query_object_list = []
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if ('LEIA' in line):
                    leia_path = line.partition('=')[2].rstrip()
                    doc = ET.parse(leia_path).getroot()
                    for q in doc.findall('QUERY'):
                        self.query_object_list.append(Query(q))
                        
    def generate_consultas(self):
        for item in self.query_object_list:
            print(f'{item.number} {item.text} {item.results} {item.records}')