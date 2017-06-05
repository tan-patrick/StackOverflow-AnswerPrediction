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
    PATH_DATA = '../../../data/%s/' % dataset
    PATH_RESULTS = '../../../results/%s/' % dataset
    
    if not os.path.exists(PATH_RESULTS):
        os.makedirs(PATH_RESULTS)

    '''                
    # load post user mapping
    uset = set()
    post_owner = {}
    for target in ['question', 'answer']:
        with open(PATH_DATA + 'posts_%s.json' % target, 'r') as fin:
            for line in fin:
                data = json.loads(line)
                post_owner[data['Id']] = data['OwnerUserId'] if 'OwnerUserId' in data else None
                if 'OwnerUserId' in data:
                    uset.add(data['OwnerUserId'])
    ulist = list(uset)
    uidx = { ulist[i]: i for i in range(len(ulist)) }

    # dump training and testing features
    for task in ['train', 'test']:
        with open(PATH_DATA + '%s.question_answer_mapping.json' % task, 'r') as fin, \
             open('%s.%s' % (dataset, task), 'w') as fout:
            for line in fin:
                data = json.loads(line)
                qid = data['QuestionId']
                try:
                    q_user = uidx[post_owner[qid]]
                except:
                    q_user = 0
                for aid in data['AnswerList']:
                    try:
                        a_user = uidx[post_owner[aid]]
                    except:
                        a_user = 0
                    print('%d %d' % (q_user, a_user), file=fout)

    num_user = len(ulist)
    '''                
    num_user = 3207438
    os.system('./bprmf/bprmf -U %s -I %s -S 1 %s.train %s.test %s.model' % (num_user, num_user, dataset, dataset, dataset))
    os.system('./bprmf/bprmf-predict %s.train %s.model %s.test %s/pred.bprmf' % (dataset, dataset, dataset, PATH_RESULTS))
    
    


