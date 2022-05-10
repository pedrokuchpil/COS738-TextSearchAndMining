from invertedlistgenerator import InvertedListGenerator
from indexer import Indexer

ind = Indexer('../config/INDEX.CFG')
#ind.generate_tf()
#ind.generate_idf()
ind.tf_idf()
print(ind.idf)