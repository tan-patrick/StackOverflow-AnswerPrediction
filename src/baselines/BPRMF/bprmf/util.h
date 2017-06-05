#pragma once

#include <cfloat>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <Eigen/Sparse>

using namespace std;

#define CERR(param, ARGS) do {\
    if(!param.quiet) cerr << ARGS;\
} while (false)

enum Norm{NORM_NONE, NORM_LINEAR, NORM_MEANVAR};

typedef Eigen::Triplet<double> Triplet;
typedef pair<int, int> MatchPair;


template<typename T, typename U>
istream& operator>>(istream &in, Eigen::Triplet<T, U> &_x) {
    U _row, _col;
    T _value;
    in >> _row >> _col >> _value;
    _x = {_row, _col, _value};
    return in;
}


void set_rand_seed(int seed);

class Parameter{
    public:
        int K, numU, numI, nSample, random_seed, norm, vAUC;
        bool quiet;
        double learning_rate, reg_user, reg_item;
        Parameter(){
            learning_rate = 0.05;
            numU = numI = -1;
            K = 10;
            nSample = 10;
            vAUC = 0;
            reg_user = 0.001;
            reg_item = 0.001;            
            quiet = false;
            norm = NORM_LINEAR;
            random_seed = 0;
        };
};


void exit_with_predict_usage();
void exit_with_usage();
int read_parameter(int argc, const char* argv[], Parameter &param);
int read_predict_parameter(int argc, const char* argv[], Parameter &param);

