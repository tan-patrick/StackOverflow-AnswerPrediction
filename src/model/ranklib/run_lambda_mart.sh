#!/bin/bash

if [ $# == 0 ]; then
    echo "usage: $0 dataset"
    exit
else
    java -jar RankLib.jar \
        -train ../../../features/$1/train.libsvm \
        -test ../../../features/$1/test.libsvm \
        -save ../../../features/$1/model.lambdamart \
        -ranker 6 -metric2t P@1 -tvs 0.8 -shrinkage 0.1
    TMP=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
    java -jar RankLib.jar \
        -rank ../../../features/$1/test.libsvm \
        -load ../../../features/$1/model.lambdamart \
        -score $TMP  
    mkdir -p ../../../results/$1/
    gawk '{ print $3 }' $TMP > ../../../results/$1/pred.lambdamart
    rm -f $TMP
    
fi

   
