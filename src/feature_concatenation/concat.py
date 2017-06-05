#!/usr/bin/env python3

import sys, os
try:
    import ujson as json
except:
    import json

if __name__ == '__main__':
    if len(sys.argv) < 1 + 2:
        print('--usage %s name_of_the_dataset config' % sys.argv[0], file=sys.stderr) 
        sys.exit(0)

    # load config
    dataset = sys.argv[1]
    config = sys.argv[2]

    PATH_DATA = '../../data/%s/' % dataset
    PATH_FEATURE = '../../features/%s/' % dataset
    
    feature_list = [ x.strip() for x in open(config, 'r').readlines() if x.strip()[0] != '#' ]


    for task in ['train', 'test']:
        qid = 0
        fin_list = [ open(PATH_FEATURE + f + '.' + task, 'r') for f in feature_list ]
        with open(PATH_DATA + '%s.question_answer_mapping.json' % task, 'r') as fin, \
             open(PATH_FEATURE + '%s.libsvm' % task, 'w') as fout:
            for line in fin:
                data = json.loads(line)
                qid += 1
                ans = data['AcceptedAnswerId']
                for aid in data['AnswerList']:
                    fout.write('1' if aid == ans else '0')
                    fout.write(' qid:%d' % qid)
                    fid = 1
                    for f in fin_list:
                        v = json.loads(f.readline())
                        if type(v) == int:
                            fout.write(' %d:%d' % (fid, v))
                            fid += 1
                        elif type(v) == float:
                            fout.write(' %d:%f' % (fid, v))
                            fid += 1
                        elif type(v) == list:
                            for val in v:
                                fout.write(' %d:%f' % (fid, val))
                                fid += 1
                        elif type(v) == dict:
                            for val in v.keys():
                                if val != 'len':
                                    fout.write(' %d:%d' % (fid + int(val), v[val]))
                            try:
                                fid += v['len']
                            except:
                                print(v)
                                sys.exit(0)
                        else:
                            print('Unrecognized feature %s' % v, file=sys.stderr)
                    fout.write('\n')

