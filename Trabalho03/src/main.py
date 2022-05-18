from queryprocessor import QueryProcessor
from invertedlistgenerator import InvertedListGenerator
from indexer import Indexer
from searcher import Searcher
from evaluator import Evaluator


qp = QueryProcessor('../config/PC.CFG')
qp.generate_consultas()
qp.generate_esperados()

ilg = InvertedListGenerator('../config/GLI.CFG')
ilg.generate_escreva()

ind = Indexer('../config/INDEX.CFG')
ind.to_json()

stem = ilg.stem and qp.stem
sea = Searcher('../config/BUSCA.CFG', stem)
sea.run_searches()

eva = Evaluator('../results/resultados-stemmer.csv', '../results/esperados.csv')