#!/usr/bin/env python3

import sys, os
import itertools
try:
    import ujson as json
except:
    import json

if __name__ == '__main__':
    """
    This file loads "posts_answer.json" and "users.json" and counts the number of times 
    user A and user B answered the same question.
    """
    if len(sys.argv) < 1 + 1:
        print('--usage python3 %s [dataset name]' % sys.argv[0], file=sys.stderr)
        sys.exit(0)

    # load the path of the dataset
    dataset = sys.argv[1]
    PATH_DATA = '../../data/%s/' % dataset
    PATH_FEATURE = '../../features/%s/' % dataset

    # check if the feature folder exists. If not, create a folder.
    if not os.path.exists(PATH_FEATURE):
        os.makedirs(PATH_FEATURE)

    # load "posts_answer.json" to count the user ID under each question.
    # Maintain an set of items like "Question ID: [Answered User1 ID, Answered User2 ID, ... ]"
    answered_user = {}
    with open(PATH_DATA + 'posts_answer.json', 'r') as fin:
        for line in fin:
            data = json.loads(line)
            try:
                if data['ParentId'] not in answered_user:
                    # There may be multiple answers from a same user under a questions.
                    answered_user[data['ParentId']] = set([int(data['OwnerUserId'])])
                else:
                    answered_user[data['ParentId']].add(int(data['OwnerUserId']))
            except:
                pass

    # Find all the user pairs that answered the same question
    user_pair = {}
    for q_id, q_user_list in answered_user.items():
        q_user_list = list(q_user_list)
        for pair in itertools.combinations(q_user_list, r=2):
            sort_pair = tuple(sorted(pair))
            if sort_pair not in user_pair:
                user_pair[sort_pair] = [q_id]
            else:
                user_pair[sort_pair].append(q_id)

    # Output the user_pair to 1 files
    #     users_common_question_count.json
    with open(PATH_DATA + "user_connection.txt", "w") as fout_count:
        for u_pair, q_list in user_pair.items():
            q_list = list(q_list)
            user_1_id, user_2_id = int(u_pair[0]), int(u_pair[1])
            print("{0} {1} {2}".format(str(user_1_id), str(user_2_id), float(len(q_list))), file=fout_count)

