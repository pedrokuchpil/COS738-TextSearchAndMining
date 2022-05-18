from email.encoders import encode_noop
import time
import pandas as pd

class Evaluator:
    def __init__(self, results_file, expecteds_file):
        self.__results_file = results_file
        self.__expecteds_file = expecteds_file
        self.__results = {}
        self.__expecteds = {}

        with open (self.__results_file, 'r', encoding='utf-8') as rf:
            next(rf)
            for line in rf:
                if line.partition(';')[0] not in self.__results:
                    self.__results[line.partition(';')[0]] = []
                self.__results[line.partition(';')[0]] .append(list(map(float,(line.partition(';')[2].replace(']', '').replace('[', '').replace('\n', '').replace("'", "").split(', ')))))
                
        df = pd.read_csv(self.__expecteds_file, sep=';', encoding='utf-8')
        df.sort_values("DocVotes", axis=0, ascending=False, inplace=True, na_position='first')
        df.to_csv(self.__expecteds_file, sep=';', encoding='utf-8', index=False)

        with open (self.__expecteds_file, 'r', encoding='utf-8') as ef:
            next(ef)
            for line in ef:
                if line.split(';')[0] not in self.__expecteds:
                    self.__expecteds[line.split(';')[0]] = []
                self.__expecteds[line.split(';')[0]].append([line.split(';')[1], line.split(';')[2].replace('\n', '')])
        
    def generate_measures(self):
        pass