#!/usr/bin/env python3

import sys, os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

try:
    import ujson as json
except:
    import json

if __name__ == '__main__':
    if len(sys.argv) < 1 + 1:
        print('--usage %s [dataset name]' % sys.argv[0], file=sys.stderr)
        sys.exit(0)
    
    # load Node2Vec data into
    dataset = sys.argv[1]
    PATH_DATA = '../../data/%s/' % dataset
    PATH_FEATURE = '../../features/%s/' % dataset

    # check and create the feature directory
    if not os.path.exists(PATH_FEATURE):
        os.makedirs(PATH_FEATURE)

    # load data from user_embedding.txt
    user_emb = {}
    emb_sum = np.zeros(100)
    with open(PATH_DATA + "user_embedding.txt", "r") as fin:
        info = fin.readline()
        user_count = int(info.split(" ")[0])
        for line in fin:
            line_split = line.split(" ")
            user_id, user_vec = line_split[0], [float(x.strip()) for x in line_split[1:]]
            user_emb[user_id] = np.array(user_vec)
            # print(user_vec)
            emb_sum += np.array(user_vec)

    # Using the average embedding as the missing embedding value
    avg_emb = emb_sum / user_count

    # before you can work on the mapping, you have to load posts first.
    qu_pair = {}
    au_pair = {}
    with open(PATH_DATA + "posts_question.json", "r") as fin_q:
        for line in fin_q:
            data = json.loads(line)
            try:
                qid, uid = data['Id'], data['OwnerUserId']
                qu_pair[qid] = uid
            except:
                pass

    with open(PATH_DATA + "posts_answer.json", "r") as fin_a:
        for line in fin_a:
            data = json.loads(line)
            try:
                aid, uid = data['Id'], data['OwnerUserId']
                au_pair[aid] = uid
            except:
                pass
    
    # dump training features
    for target in ['train', 'test']:
        with open(PATH_DATA + target + '.question_answer_mapping.json', 'r') as fin, \
             open(PATH_FEATURE + 'quser_auser_sim.' + target, 'w') as fout_sim, \
             open(PATH_FEATURE + 'quser_auser_emb.' + target, 'w') as fout_emb:
            for line in fin:
                data = json.loads(line)
                qid = data['QuestionId']
                try:
                    qu_emb = user_emb[qu_pair[qid]] # the embedding of the questioning user
                except:
                    qu_emb = avg_emb # if cannot find the embedding for any reason, take it as average
                for aid in data['AnswerList']:
                    try:
                        au_emb = user_emb[au_pair[aid]]
                    except:
                        au_emb = avg_emb
                    # For single sample vectors, reshape it using X.reshape(1,-1)
                    cos_sim = cosine_similarity(qu_emb.reshape(1,-1), au_emb.reshape(1,-1))
                    print(json.dumps(list(qu_emb) + list(au_emb)), file=fout_emb)
                    print(json.dumps([float(cos_sim)]), file=fout_sim)





