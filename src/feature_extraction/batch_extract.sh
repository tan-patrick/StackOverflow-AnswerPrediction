#!/bin/bash
#./comment_cnt.py $1
#./user_age.py $1
#./user_badge.py $1
#./user_reputation.py $1
#./user_user_interactions.py $1
#./user_views.py $1 
#./user_votes.py $1


#echo "Constructing user lists under same questions"
#./sn_user_common_question.py $1
#echo "Calculating node embeddings of each user"
#python ../../node2vec/src/main.py --input ../../data/${1}/user_connection.txt --output ../../data/${1}/user_embedding.txt --weighted --dimensions 100 
#echo "Calculating similarities and output files"
#./sn_user_sim.py $1

echo "Calculating user distances. Unconnected user distance are assigned to 10000"
./sn_user_dis.py $1


echo "Calculating nlp sentence features..."
python3 nlp_sentence.py $1
echo "Calculating nlp word features...."
python3 nlp_word.py $1

