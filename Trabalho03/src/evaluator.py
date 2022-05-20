import json
from ordered_set import OrderedSet

def to_set(results, limit):
    s = OrderedSet()
    for result in results:
        if result[2] > limit:
            s.add(result[1])
    return s

def precision(results, expecteds):
    if len(results) == 0:
        return 0
    value = len(results & expecteds) / len(results)
    return value

def recall(results, expecteds):
    if len(expecteds) == 0:
        return 0
    value = len(results & expecteds) / len(expecteds)
    return value

def f1_score(precision, recall):
    if (precision + recall) == 0:
        return 0
    return 2 * precision * recall / (precision + recall)

def precision_k(results, expecteds, k):
    return precision (results[:k-1], expecteds[:k-1])


class Evaluator:
    def __init__(self, results_file, expecteds_file):
        self.__results_file = results_file
        self.__expecteds_file = expecteds_file
        self.__results = {}
        self.__expecteds = {}

        with open (self.__results_file, 'r', encoding='utf-8') as rf:
            next(rf)
            for line in rf:
                key = int(line.partition(';')[0])
                if key not in self.__results:
                    self.__results[key] = []
                self.__results[key].append(list(map(float,(line.partition(';')[2].replace(']', '').replace('[', '').replace('\n', '').replace("'", "").split(', ')))))
        
        with open (self.__expecteds_file, 'r', encoding='utf-8') as ef:
            next(ef)
            for line in ef:
                key = int(line.partition(';')[0])
                if key not in self.__expecteds:
                    self.__expecteds[key] = []
                self.__expecteds[key].append([line.split(';')[1], line.split(';')[2].replace('\n', '')])
        
        for key in self.__expecteds:
            cont = 1
            self.__expecteds[key] = sorted(self.__expecteds[key], key=lambda x: x[1], reverse = True)
            for e in self.__expecteds[key]:
                e.insert(0, cont)
                self.__expecteds[key][cont-1] = list(map(float, e))
                cont += 1
        
        with open('expected.json', 'w', encoding='utf-8') as f:
            json.dump(self.__expecteds, f)
        
    def generate_measures(self):
        for key in self.__results:
            results_set = to_set(self.__results[key], 0.1)
            expecteds_set = to_set(self.__expecteds[key], 0.1)
            print(key)
            p = precision(results_set, expecteds_set)
            print ('Precisão: ' + str(p))
            r = recall(results_set, expecteds_set)
            print ('Recall: ' + str(r))
            f1 = f1_score(p, r)
            print ('F1: ' + str(f1))
            p5 = precision_k(results_set, expecteds_set, 5)
            print ('P@5: ' + str(p5))
            p10 = precision_k(results_set, expecteds_set, 10)
            print ('P@10: ' + str(p10))