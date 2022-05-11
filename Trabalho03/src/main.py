from queryprocessor import QueryProcessor
from invertedlistgenerator import InvertedListGenerator
from indexer import Indexer
from searcher import Searcher


qp = QueryProcessor('../config/PC.CFG')
qp.generate_consultas()
qp.generate_esperados()

ilg = InvertedListGenerator('../config/GLI.CFG')
ilg.generate_escreva()

ind = Indexer('../config/INDEX.CFG')
ind.to_json()

sea = Searcher('../config/BUSCA.CFG')
sea.run_searches()
