#!/usr/bin/env python3
import gensim
import nltk
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

	model = gensim.models.KeyedVectors.load_word2vec_format('../../model/word2vec/GoogleNews-vectors-negative300.bin', binary=True)  
	stoplist = nltk.corpus.stopwords.words('english')

	word_list_query = {}

	with open(PATH_DATA + 'posts_question.json','r') as fin:
		for line in fin:
			data = json.loads(line)
			body = data['Body'].lower().split()
			temp_body = [word for word in body if word not in stoplist]
			word_list_query[data['Id']] = temp_body[:200]


	word_list_answer= {}
	with open(PATH_DATA + 'posts_answer.json','r') as fin:
		for line in fin:
			data = json.loads(line)
			body = data['Body'].lower().split()
			temp_body = [w for w in body if word not in stoplist]
			word_list_answer[data['Id']] = temp_body[:200]

	with open(PATH_DATA + 'train.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'word2vec_q_a_sim.train', 'w') as fout1, \
         open(PATH_FEATURE + 'word2vec_a_a_sim.train', 'w') as fout2:

         for line in fin:
         	data = json.loads(line)
         	for aid in data['AnswerList']:
         		qid = data['QuestionId']
         		sentence_aid = word_list_answer[aid]
         		sentence_qid = word_list_query[qid]
         		print(json.dumps(model.wmdistance(sentence_aid,sentence_qid)), file=fout1)

         		total_dis = 0.0
         		for other_aid in data['AnswerList']:
         			other_sentence_aid = word_list_answer[aid]
         			total_dis += model.wmdistance(sentence_aid,other_sentence_aid)

         		print(json.dumps(total_dis/float(len(data['AnswerList']))), file = fout2)



    with open(PATH_DATA + 'test.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'word2vec_q_a_sim.test', 'w') as fout1, \
         open(PATH_FEATURE + 'word2vec_a_a_sim.test', 'w') as fout2:

         for line in fin:
         	data = json.loads(line)
         	for aid in data['AnswerList']:
         		qid = data['QuestionId']
         		sentence_aid = word_list_answer[aid]
         		sentence_qid = word_list_query[qid]
         		print(json.dumps(model.wmdistance(sentence_aid,sentence_qid)), file=fout1)

         		total_dis = 0.0
         		for other_aid in data['AnswerList']:
         			other_sentence_aid = word_list_answer[aid]
         			total_dis += model.wmdistance(sentence_aid,other_sentence_aid)

         		print(json.dumps(total_dis/float(len(data['AnswerList']))), file = fout2)


















