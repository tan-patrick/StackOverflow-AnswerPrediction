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
    

    # load age of every user
    age_sum = num = 0
    user_age = {}
    with open(PATH_DATA + 'users.json', 'r') as fin:
        for line in fin:
            data = json.loads(line)
            age = int(data['Age']) if 'Age' in data else None
            if age != None:
                user_age[data['Id']] = age
                age_sum += age
                num += 1
    avg_age = age_sum / num

    # load post user mapping
    post_owner = {}
    for target in ['question', 'answer']:
        with open(PATH_DATA + 'posts_%s.json' % target, 'r') as fin:
            for line in fin:
                data = json.loads(line)
                post_owner[data['Id']] = data['OwnerUserId'] if 'OwnerUserId' in data else None


    # dump training features
    with open(PATH_DATA + 'train.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'user_age.train', 'w') as fout:
        for line in fin:
            data = json.loads(line)
            qid = data['QuestionId']
            try:
                q_user = post_owner[qid]
                q_age = user_age[q_user]
            except:
                q_age = avg_age
            for aid in data['AnswerList']:
                try:
                    a_user = post_owner[aid]
                    a_age = user_age[a_user] 
                except:
                    a_age = avg_age
                print(json.dumps([q_age, a_age]), file=fout)
                
    # dump testing features
    with open(PATH_DATA + 'test.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'user_age.test', 'w') as fout:
        for line in fin:
            data = json.loads(line)
            qid = data['QuestionId']
            try:
                q_user = post_owner[qid]
                q_age = user_age[q_user]
            except:
                q_age = avg_age
            for aid in data['AnswerList']:
                try:
                    a_user = post_owner[aid]
                    a_age = user_age[a_user] 
                except:
                    a_age = avg_age
                print(json.dumps([q_age, a_age]), file=fout)
