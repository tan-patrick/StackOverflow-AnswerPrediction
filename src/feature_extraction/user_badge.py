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
    

    # load badge of every user
    badge_set = set()
    user_badge = {}
    with open(PATH_DATA + 'badges.json', 'r') as fin:
        for line in fin:
            data = json.loads(line)
            uid = data['UserId']
            badge = data['Name']
            if uid not in user_badge:
                user_badge[uid] = []
            user_badge[uid].append(badge)
            badge_set.add(badge)

    num_badge = len(badge_set)
    badge_list = list(badge_set)
    badge_idx = {badge_list[i]: i for i in range(len(badge_list))}

    # load post user mapping
    post_owner = {}
    for target in ['question', 'answer']:
        with open(PATH_DATA + 'posts_%s.json' % target, 'r') as fin:
            for line in fin:
                data = json.loads(line)
                post_owner[data['Id']] = data['OwnerUserId'] if 'OwnerUserId' in data else None

    # dump training features
    with open(PATH_DATA + 'train.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'user_badge.train', 'w') as fout:
        for line in fin:
            data = json.loads(line)
            qid = data['QuestionId']
            q_fea = {}
            try:
                q_user = post_owner[qid]
                for b in user_badge[q_user]:
                    q_fea[badge_idx[b]] = 1
            except:
                pass            

            q_fea['len'] = num_badge * 2
            for aid in data['AnswerList']:
                fea = q_fea 
                try:
                    a_user = post_owner[aid]
                    for b in user_badge[a_user]:
                        fea[badge_idx[b]] = 1
                except:
                    pass
                print(json.dumps(fea), file=fout)
                
    # dump testing features
    with open(PATH_DATA + 'test.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'user_badge.test', 'w') as fout:
        for line in fin:
            data = json.loads(line)
            qid = data['QuestionId']
            q_fea = {}
            try:
                q_user = post_owner[qid]
                for b in user_badge[q_user]:
                    q_fea[badge_idx[b]] = 1
            except:
                pass            

            q_fea['len'] = num_badge * 2
            for aid in data['AnswerList']:
                fea = q_fea 
                try:
                    a_user = post_owner[aid]
                    for b in user_badge[a_user]:
                        fea[badge_idx[b]] = 1
                except:
                    pass
                print(json.dumps(fea), file=fout)
