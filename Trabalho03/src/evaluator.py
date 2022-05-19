from email.encoders import encode_noop
import json
def to_set(results, limit):
    s = set()
    for result in results:
        if result[2] > limit:
            s.add(result[1])
    return s


def precision(results, expecteds):
    if len(results) > 0:
        value = len(results & expecteds) / len(results)
    else:
        value = 0
    return value

def recall(results, expecteds):
    value = len(results & expecteds) / len(expecteds)
    return value


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
            print ('Precisão: ' + str(precision(results_set, expecteds_set)))