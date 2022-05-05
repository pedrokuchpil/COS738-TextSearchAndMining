import os
import re
from xml.etree import ElementTree as ET

class Query:
    def __init__(self, record):
        self.number = int(record.find('QueryNumber').text)
        self.text = re.sub("[^a-zA-Z] ", "", record.find('QueryText').text).replace('\n', ' ').upper()
        self.results = 0
        self.records = []

query_object_list = []

def read_config(file):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if ('LEIA' in line):
                leia_path = line.partition('=')[2].rstrip()
                doc = ET.parse(leia_path).getroot()
                for record in doc.findall('QUERY'):
                    query_object_list.append(Query(record))
                for item in query_object_list:
                    print(f'{item.number} {item.text}')