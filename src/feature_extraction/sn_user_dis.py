#!/usr/bin/env python3

import sys, os
import networkx as nx
try:
    import ujson as json
except:
    import json

"""
Construct an Graph using networkx. Compute the shortest-path of each pair of nodes.
"""
if __name__ == "__main__":
    # check the input dataset name
    if len(sys.argv) < 1 + 1:
        print('--usage python %s [dataset name]' % sys.argv[0], file=sys.stderr)
        sys.exit(0) 

    # load the path of dataset
    dataset = sys.argv[1]
    PATH_DATA = '../../data/%s/' % dataset
    PATH_FEATURE = '../../features/%s/' % dataset

    # check if feature directory exists, if not then create it
    if not os.path.exists(PATH_FEATURE):
        os.makedirs(PATH_FEATURE)

    # load "user_connection.txt" and generate a graph of the network using NetworkX
    G = nx.Graph()
    with open(PATH_DATA + "user_connection.txt", "r") as fin:
        for line in fin:
            line_split = line.split(" ")
            # The line format is "uid1 uid2 #_of_common_questions_answered"
            uid1, uid2 = int(line_split[0]), int(line_split[1])
            # Use the inverse of a number as the weight
            weight = 1 / float(line_split[2].strip())
            G.add_edge(uid1, uid2, weight=weight)
    
    ndset = set(nx.nodes(G))

    # Load Question-User pair and Answer-User pair
    qu = {}
    au = {}
    with open(PATH_DATA + 'posts_question.json', 'r') as fin_q, \
         open(PATH_DATA + 'posts_answer.json', 'r') as fin_a:
             for line in fin_q:
                 data = json.loads(line)
                 try:
                    qid, uid = data['Id'], data['OwnerUserId']
                    qu[qid] = uid
                 except:
                     pass
             for line in fin_a:
                 data = json.loads(line)
                 try:
                     aid, uid =data['Id'], data['OwnerUserId']
                     au[aid] = uid
                 except:
                     pass

    # Load Question-Answer Mapping
    dis_st_frm = {}
    for target in ['train', 'test']:
        with open(PATH_DATA + target + ".question_answer_mapping.json", "r") as fin:
            with open(PATH_FEATURE + "qu_au_dis." + target, "w") as fout:
                for line in fin:
                    data = json.loads(line)
                    try:
                        q_uid = int(qu[data['QuestionId']])
                    except:
                        # Some post may lack OwnerUserId, if cannot find uid from a post, then set q_uid to -1.
                        q_uid = -1
                    try:
                        if q_uid != -1 and q_uid not in dis_st_frm:
                            dis_st_frm[q_uid] = nx.single_source_dijkstra_path_length(G, q_uid)
                    except:
                        pass

                    for aid in data['AnswerList']:
                        try:
                            a_uid = int(au[aid])
                        except:
                            # Some post may lack OwnerUserId, if cannot find uid from a post, then set a_uid to -1.
                            a_uid = -1
                        
                        try:
                            # dij_dis = nx.dijkstra_path_length(G, source=int(q_uid), target=int(a_uid))
                            dij_dis = dis_st_frm[q_uid][a_uid]
                        except:
                            dij_dis = 100000
                        print(json.dumps([dij_dis]), file=fout)
