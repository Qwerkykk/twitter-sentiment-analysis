
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.manifold import TSNE
from wordcloud import WordCloud, STOPWORDS

class Visualizer:

    def __init__(self, preprocessor):

        self.preprocessor = preprocessor


    def visualize(self, labels=['positive', 'negative', 'neutral'], method='cloud'):
        
        tokens = []

        for label in set(labels):
            if label not in self.preprocessor.tweets.keys():
                raise ValueError("'" + label + "' is not a valid label")
            else:
                tokens += [token for tweet in self.preprocessor.tweets[label] for token in tweet]

        if method == 'cloud':
            return self.cloud(tokens)
        elif method == 'frame':
            return self.frame(tokens)
        else:
            raise ValueError("'" + method + "' does not name any visualization method")


    @staticmethod
    def frame(tokens):
        
        count = Counter(tokens)

        dataFrame = pd.DataFrame(data=count.most_common(50), columns=['Word', 'Count'])

        print(dataFrame)

        return dataFrame


    @staticmethod
    def cloud(tokens):

        wordcloud = WordCloud(width = 1200, height = 1200,
                background_color ='white',
                stopwords = set(STOPWORDS),
                min_font_size = 14).generate(' '.join(tokens))

        plt.figure(figsize = (8, 8), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        plt.show()

        return wordcloud

    @staticmethod
    def tsne(model):
        from itertools import islice
        labels = []
        tokens = []
        counter = 0

        for word in model.wv.vocab:
            tokens.append(model[word])
            labels.append(word)
            counter +=1
            if counter == 300:
                break

        tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=5000, random_state=23,)
        new_values = tsne_model.fit_transform(tokens)

        x = []
        y = []

        for value in new_values:
            x.append(value[0])
            y.append(value[1])

        plt.figure(figsize=(16, 16)) 
        for i in range(len(x)):
            plt.scatter(x[i],y[i])
            plt.annotate(labels[i],
                xy=(x[i], y[i]),
                xytext=(5, 2),
                textcoords='offset points',
                ha='right',
                va='bottom')
        plt.show()

