#!/usr/bin/env python3

import trueskill
import random, string
import sys, os
try:
    import ujson as json
except:
    import json

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text_list):
    tfidf = vectorizer.fit_transform(text_list)
    return ((tfidf * tfidf.T).A)[0,1:]

if __name__ == '__main__':

    if len(sys.argv) < 1 + 1:
        print('--usage %s name_of_the_dataset' % sys.argv[0], file=sys.stderr) 
        sys.exit(0)

    # load 
    dataset = sys.argv[1]
    PATH_DATA = '../../data/%s/' % dataset
    PATH_FEATURE = '../../features/%s/' % dataset

    # check and create the feature directory for the dataset
    if not os.path.exists(PATH_FEATURE):
        os.makedirs(PATH_FEATURE)

    # load required post ids
    required_ids = set()
    for task in ['train', 'test']:
        with open(PATH_DATA + '%s.question_answer_mapping.json' % task, 'r') as fin:
            for line in fin:
                data = json.loads(line) 
                required_ids.add(data['QuestionId'])
                for aid in data['AnswerList']:
                    required_ids.add(aid)

    # produce the text mapping
    post_body = {}
    for target in ['question', 'answer']:
        with open(PATH_DATA + 'posts_%s.json' % target, 'r') as fin:
            for line in fin:
                data = json.loads(line)
                if data['Id'] in required_ids:
                    post_body[data['Id']] = data['Body']
    
    # dump training and testing features
    for task in ['train', 'test']:
        with open(PATH_DATA + '%s.question_answer_mapping.json' % task, 'r') as fin, \
             open(PATH_FEATURE + 'text_cos_sim.%s' % task, 'w') as fout:
            for line in fin:
                data = json.loads(line)
                qid = data['QuestionId']
                text_list = []
                text_list.append(post_body[qid] if qid in post_body else '')
                for aid in data['AnswerList']:
                    text_list.append(post_body[aid] if aid in post_body else '')
                sim = cosine_sim(text_list)
                for x in sim:
                    print(x, file=fout)
                
