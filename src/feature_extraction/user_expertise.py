#!/usr/bin/env python3

import trueskill
import random
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
    
    # load post user mapping
    post_owner = {}
    for target in ['question', 'answer']:
        with open(PATH_DATA + 'posts_%s.json' % target, 'r') as fin:
            for line in fin:
                data = json.loads(line)
                post_owner[data['Id']] = data['OwnerUserId'] if 'OwnerUserId' in data else None

    # load competitions 
    list_comp = []
    with open(PATH_DATA + 'train.question_answer_mapping.json', 'r') as fin:
        for line in fin:
            data = json.loads(line)
            qid = data['QuestionId']
            q_user = post_owner[qid]
            try:
                best_user = post_owner[data['AcceptedAnswerId']]
                # best answerer is better than the questioner
                list_comp.append((best_user, q_user))

                for aid in data['AnswerList']:
                    if aid != best_user: 
                        # best answerer is better than other answerers 
                        list_comp.append((best_user, aid))
            except:
                pass

    # random shuffle and conduct competitions
    random.shuffle(list_comp)
    user_rating = {}
    for user_w, user_l in list_comp:
        rw = user_rating[user_w] if user_w in user_rating else trueskill.Rating()
        rl = user_rating[user_l] if user_l in user_rating else trueskill.Rating()
        rw, rl = trueskill.rate_1vs1(rw, rl)
        user_rating[user_w] = rw
        user_rating[user_l] = rl


    # load post user mapping
    post_owner = {}
    for target in ['question', 'answer']:
        with open(PATH_DATA + 'posts_%s.json' % target, 'r') as fin:
            for line in fin:
                data = json.loads(line)
                post_owner[data['Id']] = data['OwnerUserId'] if 'OwnerUserId' in data else None


    # dump training and testing features
    for task in ['train', 'test']:
        with open(PATH_DATA + '%s.question_answer_mapping.json' % task, 'r') as fin, \
             open(PATH_FEATURE + 'user_expertise.%s' % task, 'w') as fout:
            for line in fin:
                data = json.loads(line)
                qid = data['QuestionId']
                try:
                    q_user = post_owner[qid]
                    q_rating = user_rating[q_user]
                except:
                    q_rating = trueskill.Rating()
                for aid in data['AnswerList']:
                    try:
                        a_user = post_owner[aid]
                        a_rating = user_rating[a_user]
                    except:
                        a_rating = trueskill.Rating()
                    print(json.dumps([q_rating.mu, a_rating.mu]), file=fout)
                
