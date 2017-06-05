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

    # load post user mapping
    post_owner = {}
    for target in ['question', 'answer']:
        with open(PATH_DATA + 'posts_%s.json' % target, 'r') as fin:
            for line in fin:
                data = json.loads(line)
                post_owner[data['Id']] = data['OwnerUserId'] if 'OwnerUserId' in data else None

    # load comments
    comment_pairs = {}
    with open(PATH_DATA + 'comments.json', 'r') as fin:
        for line in fin:
            data = json.loads(line)
            if 'UserId' in data and 'PostId' in data:
                commenter_uid = data['UserId']
                post_id = data['PostId']
                poster_uid = post_owner[post_id] if post_id in post_owner else None
                if poster_uid != None and commenter_uid != None:
                    if int(poster_uid) > int(commenter_uid):
                        temp = poster_uid
                        poster_uid = commenter_uid
                        commenter_uid = poster_uid

                    if (poster_uid, commenter_uid) in comment_pairs:
                        comment_pairs[(poster_uid, commenter_uid)] += 1
                    else:
                        comment_pairs[(poster_uid, commenter_uid)] = 1

    # dump training features
    with open(PATH_DATA + 'train.question_answer_mapping.json', 'r') as fin, \
            open(PATH_FEATURE + 'user_user_interactions.train', 'w') as fout:
        for line in fin:
            data = json.loads(line)
            qid = data['QuestionId']
            q_user = post_owner[qid]

            for aid in data['AnswerList']:
                a_user = post_owner[aid]
                pairs = comment_pairs[(q_user, a_user)] if (q_user, a_user) in comment_pairs else 0

                print(json.dumps(pairs), file=fout)

    # dump testing features
    with open(PATH_DATA + 'test.question_answer_mapping.json', 'r') as fin, \
            open(PATH_FEATURE + 'user_user_interactions.test', 'w') as fout:
        for line in fin:
            data = json.loads(line)
            qid = data['QuestionId']
            q_user = post_owner[qid]

            for aid in data['AnswerList']:
                a_user = post_owner[aid]
                pairs = comment_pairs[(q_user, a_user)] if (q_user, a_user) in comment_pairs else 0

                print(json.dumps(pairs), file=fout)
