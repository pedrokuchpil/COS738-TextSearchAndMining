from invertedlistgenerator import InvertedListGenerator
from indexer import Indexer

ind = Indexer('../config/INDEX.CFG')
print(ind.generate_tf())