#!/usr/bin/env python3


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
    
    sentence_count = {}
    avg_sentence_length = {}

    with open(PATH_DATA + 'posts_answer.json','r') as fin:
        for line in fin:
            data = json.loads(line)
            body_split = data['Body'].split('.') if 'Body' in data else []
            sentence_count[data['Id']] = len(body_split) 
            avg_sentence_length[data['Id']] = sum(len(x.split(' ')) for x in body_split) / float(len(body_split)) if len(body_split) != 0 else 0

    # dump training features
    with open(PATH_DATA + 'train.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'sentence_cnt.train', 'w') as fout, \
         open(PATH_FEATURE + 'sentence_avg_len.train','w') as fout2:
        for line in fin:
            data = json.loads(line)
            for aid in data['AnswerList']:
                print(json.dumps(sentence_count[aid]), file=fout)
                print(json.dumps(avg_sentence_length[aid]),file = fout2)


                
    # dump testing features
    with open(PATH_DATA + 'test.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'sentence_cnt.test', 'w') as fout, \
         open(PATH_FEATURE + 'sentence_avg_len.test','w') as fout2:
        for line in fin:
            data = json.loads(line)
            for aid in data['AnswerList']:
                print(json.dumps(sentence_count[aid]), file=fout)
                print(json.dumps(avg_sentence_length[aid]),file = fout2)
