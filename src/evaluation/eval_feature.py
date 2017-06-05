#!/usr/bin/env python3

import sys, os

try:
    import ujson as json
except:
    import json

if __name__ == '__main__':
    if len(sys.argv) < 1 + 2:
        print('--usage %s dataset feature' % sys.argv[0], file=sys.stderr) 
        sys.exit(0)

    # load 
    dataset = sys.argv[1]
    method = sys.argv[2]
    if len(sys.argv) >= 1 + 3:
        idx = int(sys.argv[3])
    PATH_DATA = '../../data/%s/' % dataset
    PATH_FEATURES = '../../features/%s/' % dataset
    
    # [[total P@1, total MRR], # of ins]
    p_overall =   [[0.0, 0.0], 0.0]
    p_size =  [ [[0.0, 0.0], 0.0] for i in range(3) ] # 2~5, 6~10, 10+

    # calc performance
    with open(PATH_DATA + 'test.question_answer_mapping.json', 'r') as fin, \
        open(PATH_FEATURES + '%s.test' % method, 'r') as fres:
        for line in fin:
            data = json.loads(line)
            acid = data['AcceptedAnswerId']
            pred = []
            for aid in data['AnswerList']:
                v = json.loads(fres.readline())
                if type(v) == int or type(v) == float:
                    f = v
                elif type(v) == list:
                    f = v[idx]
                else:
                    print('Do not support %s features' % str(type(v)), file=sys.stderr)
                    sys.exit(0)

                pred.append((f, aid == acid))
            pred = sorted(pred, key=lambda x: -x[0])
            szid = 0 if len(pred) <= 2 else (1 if len(pred) <= 5 else 2)
            
            p_overall[1] += 1.0
            p_size[szid][1] += 1.0
            if pred[0][1]:
                p_overall[0][0] += 1.0
                p_size[szid][0][0] += 1.0
            for i in range(len(pred)):
                if pred[i][1]:
                    p_overall[0][1] += 1.0 / float(i + 1)
                    p_size[szid][0][1] += 1.0 / float(i + 1)

    
    print('P@1\nMRR')
    print('Overall Performance')
    print(p_overall[0][0] / p_overall[1])
    print(p_overall[0][1] / p_overall[1])
    
    size_info = ['2 answers', '3 to 5 answers', 'more than 5 answers']
    for i in range(3):
        print(size_info[i])
        print(p_size[i][0][0] / p_size[i][1])
        print(p_size[i][0][1] / p_size[i][1])
        

    print('Size Distribution')
    for i in range(3):
        print('%d%s' % (p_size[i][1], '\n' if i == 2 else ':'), end='')





            
            
            
            
