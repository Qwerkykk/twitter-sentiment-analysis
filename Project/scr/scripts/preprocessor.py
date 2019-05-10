
import os
import sys
import re
import string

from nltk import word_tokenize
from nltk.corpus import stopwords

from util import platform

class Preprocessor:

    urlregex = r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''
    tagregex = r'''@[^\s]+'''

    def __init__(self, filename, cruncher, save=True):

        filename = platform.path(filename)

        if not os.path.isdir('out'):
            os.mkdir('out')

        self.filename, _ = os.path.splitext(os.path.basename(filename))

        self.filename = os.path.join(os.path.curdir, 'out', self.filename)

        self.tweets = {
            'positive': [],
            'negative': [],
            'neutral' : [],
            'unknown' : []
        }

        for label in self.tweets.keys():

            if not os.path.isfile(self.filename + '_' + label + '.tsv'):

                with open(filename, mode='r', encoding='utf8') as file:
                    lines = file.readlines()

                ignore = set(stopwords.words('english'))

                for line in lines:
                    # Remove any non ascii characters (for example emojis)
                    line = line.encode('ascii', 'ignore').decode('ascii')

                    # Remove any leading and trailing whitespace characters
                    line = line.strip()

                    # Convert every character to its lower case counterpart
                    line = line.lower()

                    # Remove any urls
                    line = re.sub(self.urlregex, '', line)

                    # Remove any tags
                    line = re.sub(self.tagregex, '', line)

                    # Remove any punctuation
                    line = line.translate(str.maketrans('', '', string.punctuation))

                    # Tokenize tweet at hand and lemmatize each one of its tokens
                    # while removing any stopwords
                    tokens = word_tokenize(line)

                    tokens = [cruncher.crunch(token) for token in tokens if token not in ignore]

                    if tokens[2] in self.tweets.keys():
                        self.tweets[tokens[2]].append(tokens[3:])
                    else:
                        raise ValueError("'" + tokens[2] + "' is not a valid label")

                if save:
                    for label in self.tweets.keys():
                        filename = self.filename + '_' + label + '.tsv'

                        print('<LOG>: Saving', str(len(self.tweets[label])), "'" + label +"'", 'tweets to', filename, file=sys.stderr)

                        with open(filename, 'w', encoding='ascii') as file:
                            file.write('\n'.join([label + '\t' + ' '.join(tweet) for tweet in self.tweets[label]]))

                return

        for label in self.tweets.keys():
            with open(self.filename + '_' + label + '.tsv', mode='r', encoding='ascii') as file:
                lines = file.readlines()

                self.tweets[label] = [word_tokenize(line)[1:] for line in lines]

                print('<LOG>: Loaded', str(len(lines)), "'" + label + "'", 'tweets', file=sys.stderr)

