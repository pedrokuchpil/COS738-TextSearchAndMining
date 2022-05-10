class Searcher:

    def __init__(self, file):
            self.__modelo_path = ''
            self.__consultas_path = ''
            self.__resultados_path = ''
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    if ('MODELO' in line):
                        self.__modelo_path = line.partition('=')[2].rstrip()
                    elif ('CONSULTAS' in line):
                        self.__consultas_path = line.partition('=')[2].rstrip()
                    elif ('RESULTADOS' in line):
                        self.__resultados_path = line.partition('=')[2].rstrip()
    