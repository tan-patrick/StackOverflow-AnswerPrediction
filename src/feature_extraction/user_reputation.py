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
    

    # load reputation of every user
    reputation_sum = num = 0
    user_reputation = {}
    with open(PATH_DATA + 'users.json', 'r') as fin:
        for line in fin:
            data = json.loads(line)
            reputation = int(data['Reputation']) if 'Reputation' in data else None
            if reputation != None:
                user_reputation[data['Id']] = reputation
                reputation_sum += reputation
                num += 1
    reputation_avg = reputation_sum / num

    # load post user mapping
    post_owner = {}
    for target in ['question', 'answer']:
        with open(PATH_DATA + 'posts_%s.json' % target, 'r') as fin:
            for line in fin:
                data = json.loads(line)
                post_owner[data['Id']] = data['OwnerUserId'] if 'OwnerUserId' in data else None


    # dump training features
    with open(PATH_DATA + 'train.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'user_reputation.train', 'w') as fout:
        for line in fin:
            data = json.loads(line)
            qid = data['QuestionId']
            try:
                q_user = post_owner[qid]
                q_rep = user_reputation[q_user]
            except:
                q_rep = reputation_avg
            for aid in data['AnswerList']:
                try:
                    a_user = post_owner[aid]
                    a_rep = user_reputation[a_user]
                except:
                    a_rep = reputation_avg
                print(json.dumps([q_rep, a_rep]), file=fout)
                
    # dump testing features
    with open(PATH_DATA + 'test.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'user_reputation.test', 'w') as fout:
        for line in fin:
            data = json.loads(line)
            qid = data['QuestionId']
            try:
                q_user = post_owner[qid]
                q_rep = user_reputation[q_user]
            except:
                q_rep = reputation_avg
            for aid in data['AnswerList']:
                try:
                    a_user = post_owner[aid]
                    a_rep = user_reputation[a_user]
                except:
                    a_rep = reputation_avg
                print(json.dumps([q_rep, a_rep]), file=fout)
