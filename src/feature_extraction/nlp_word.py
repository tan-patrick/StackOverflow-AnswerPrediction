#!/usr/bin/env python3
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
from collections import defaultdict
import sys, os
try:
    import ujson as json
except:
    import json




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
	
	corpus_ori = []
	qid_ori = []
	with open(PATH_DATA + 'posts_question.json','r') as fin:
		for line in fin:
    		data = json.loads(line)
    		corpus_ori.append(data['Body'])
    		qid_ori.append(data['Id'])

	stoplist = nltk.corpus.stopwords.words('english')
	corpus = [[word for word in doc.lower().split(' ') if word not in stoplist] for doc in corpus_ori]
	frequency = defaultdict(int)

	for doc in corpus:
		for token in doc:
			frequency[token] += 1

	corpus = [[token for token in doc if frequency[token] > 10] for doc in corpus]
	dictionary = corpora.Dictionary(corpus)
	corpus = [dictionary.doc2bow(doc) for doc in corpus]
	tfidf = models.TfidfModel(corpus)
	tfidf_question = {}


	for doc,qid in zip(corpus_ori,qid_ori):
		new_vec = dictionary.doc2bow(doc.lower().split(' '))
		tfidf_question[qid] = tfidf[new_vec]

	stopWordCount = {}
	wordCount = {}
	tfidf_answer = {}
	tfidf_sum = {}
	max_index = 0


	with open(PATH_DATA + 'posts_answer.json','r') as fin:
		for line in fin:
			data = json.loads(line)
			body = data['Body']
			wordCount[data['Id']] = len(body.split(' '))
			stopWordCount[data['Id']]  = len([word for word in body.lower().split(' ') if word in stoplist])
			new_vec = dictionary.doc2bow(body.lower().split(' '))
			tfidf_answer[data['Id']] = tfidf[new_vec]
			total = 0.0
			for (key,val) in tfidf_answer[data['Id']]:
				total += val
				if key > max_index:
					max_index = key
			tfidf_sum[data['Id']] = total
	#index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=max_index+1)





	# dump training features
	with open(PATH_DATA + 'train.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'stopWord_cnt.train', 'w') as fout1, \
         open(PATH_FEATURE + 'word_cnt.train','w') as fout2, \
         open(PATH_FEATURE + 'tfidf_vec.train','w') as fout3, \
         open(PATH_FEATURE + 'tfidf_sum.train','w') as fout4:

         for line in fin:
         	data = json.loads(line)
         	for aid in data['AnswerList']:
         		qid = data['QuestionId']
         		print(json.dumps(stopWordCount[aid]), file=fout1)
         		print(json.dumps(wordCount[aid]),file = fout2)
         		print(json.dumps(tfidf_question[qid],tfidf_answer[aid]),file = fout3)
         		print(json.dumps(wordCount[aid]),file = fout4)

    # dump testing features
	with open(PATH_DATA + 'test.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'stopWord_cnt.test', 'w') as fout1, \
         open(PATH_FEATURE + 'word_cnt.test','w') as fout2, \
         open(PATH_FEATURE + 'tfidf_vec.test','w') as fout3, \
         open(PATH_FEATURE + 'tfidf_sum.test','w') as fout4:

         for line in fin:
         	data = json.loads(line)
         	for aid in data['AnswerList']:
         		qid = data['QuestionId']
         		print(json.dumps(stopWordCount[aid]), file=fout1)
         		print(json.dumps(wordCount[aid]),file = fout2)
         		print(json.dumps(tfidf_question[qid],tfidf_answer[aid]),file = fout3)
         		print(json.dumps(tfidf_sum[aid]),file = fout4)
         		
