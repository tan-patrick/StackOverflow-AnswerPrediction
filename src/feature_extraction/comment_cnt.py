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
    post_comment_cnt = {}
    with open(PATH_DATA + 'posts_answer.json', 'r') as fin:
        for line in fin:
            data = json.loads(line)
            post_comment_cnt[data['Id']] = int(data['CommentCount']) if 'CommentCount' in data else 0


    # dump training features
    with open(PATH_DATA + 'train.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'comment_cnt.train', 'w') as fout:
        for line in fin:
            data = json.loads(line)
            for aid in data['AnswerList']:
                print(json.dumps(post_comment_cnt[aid]), file=fout)
                
    # dump testing features
    with open(PATH_DATA + 'test.question_answer_mapping.json', 'r') as fin, \
         open(PATH_FEATURE + 'comment_cnt.test', 'w') as fout:
        for line in fin:
            data = json.loads(line)
            for aid in data['AnswerList']:
                print(json.dumps(post_comment_cnt[aid]), file=fout)
