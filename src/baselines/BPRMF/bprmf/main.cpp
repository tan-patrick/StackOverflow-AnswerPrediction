#include <fstream>
#include <iostream>
#include "error.h"
#include "matrix.h"
#include "train.h"
#include "util.h"
using namespace std;


int main(int argc, char *argv[]) {
    if (argc != 1 + 9) {
        ERR_EXIT("Format error.\n"
                 "(Usage: %s R1_train R1_valid R2_train R2_valid R2_test "
                 "match_user match_item eta_basic eta_lc)\n",
                 argv[0]);
    }

    set_rand_seed();

    SparseMatrix r1_train = read_sparse_matrix(argv[1]);
    SparseMatrix r1_valid = read_sparse_matrix(argv[2]);
    SparseMatrix r2_train = read_sparse_matrix(argv[3]);
    SparseMatrix r2_valid = read_sparse_matrix(argv[4]);
/*
    SparseMatrix r2_test = read_sparse_matrix(argv[5]);

    Matching match_user = read_matching(argv[6]);
    Matching match_item = read_matching(argv[7]);
*/
    //cerr << match_user << endl;

    const int latent_size = 30;
    const double learning_rate = atof(argv[8]);
    const double reg_user_coef = 0.02;
    const double reg_item_coef = 0.02;
    const int max_iter = 500;

    const double learning_rate_lc = atof(argv[9]);
    const double reg_user_coef_lc = 1e-8;
    const double reg_item_coef_lc = 1e-8;

    pair<Matrix, Matrix> stg1_res = basic_mf(r1_train,
                                             r1_valid,
                                             latent_size,
                                             learning_rate,
                                             reg_user_coef,
                                             reg_item_coef,
                                             max_iter
    );

    pair<Matrix, Matrix> stg2_res =     lcmf(r2_train,
                                             r2_valid,
                                             stg1_res.first,
                                             stg1_res.second,
                                             latent_size,
                                             learning_rate_lc,
                                             reg_user_coef_lc,
                                             reg_item_coef_lc,
                                             max_iter
    );

    return 0;
}
