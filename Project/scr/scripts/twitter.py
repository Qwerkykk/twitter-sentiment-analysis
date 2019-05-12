
from cruncher import Cruncher
from preprocessor import Preprocessor
from visualizer import Visualizer
from vectorizer import Vectorizer

import roundRobin as RR

if __name__ == "__main__":

    preprocessor = Preprocessor('../train.tsv', Cruncher())

    #visualization = Visualizer(preprocessor).visualize()

    for method in ['word-2-vec']:
        knownVectors = Vectorizer(method).vectorize(preprocessor)
    
    preprocessor1 = Preprocessor('../test2017.tsv', Cruncher())


    for method in ['word-2-vec']:
        unknownVectors = Vectorizer(method).vectorize(preprocessor1)

    RR.roundRobin(preprocessor.labels,knownVectors, unknownVectors)

    #model = Vectorizer(preprocessor).vectorize()
    
    #Visualizer(preprocessor).tsne(model)

