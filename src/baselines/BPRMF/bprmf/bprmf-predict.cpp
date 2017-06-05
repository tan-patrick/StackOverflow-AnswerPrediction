#include <fstream>
#include <iostream>
#include "error.h"
#include "matrix.h"
#include "model.h"
#include "util.h"
using namespace std;
int main(int argc,const char* argv[]){
    if( argc < 1 + 4){
        exit_with_predict_usage();
    }    
    
    char* train_file = NULL;
    char* valid_file = NULL;
    char* model_file = NULL;
    char* test_file = NULL;
    char* pred_file = NULL;
    Parameter param;

    /** Load parameters **/
    int train_idx = read_parameter(argc, argv, param);
    train_file = (char*) argv[train_idx++];
    model_file = (char*) argv[train_idx++];
    test_file = (char*) argv[train_idx++];
    if(train_idx!=argc){
        pred_file = (char*)argv[train_idx];
    }
    
    /** Set Random Seed **/
    set_rand_seed(param.random_seed);

    /** File Description **/
    if(pred_file == NULL){
        pred_file = new char[ strlen(test_file) + 10 ];
        sprintf(pred_file,"%s.pred",test_file);
    }

    CERR(param, "Train File = " << train_file << endl);
    CERR(param, "Model File = " << model_file << endl);
    CERR(param, "Test  File = "  << test_file << endl);

    /** Load Data **/
    CERR(param, "Load train, valid and test matrices...");
    vector<UIpair> train_mat = read_oneclass_matrix(train_file, param);
    vector<UIpair> test_mat = read_oneclass_matrix(test_file, param);
    CERR(param, "Done!" << endl);

    /** Load Model **/
    pair<Matrix, Matrix> model = read_bprmf(model_file, param);
    ASSERT( model.first.rows() == param.K );
    ASSERT( model.first.cols() == param.numU );
    ASSERT( model.second.rows() == param.K );
    ASSERT( model.second.cols() == param.numI );

    CERR(param, "(numU, numI, K) = ("
        << param.numU << ", "
        << param.numI << ", "
        << param.K << ")" << endl);
    
    Matrix P = model.first;
    Matrix Q = model.second;
    ofstream wp(pred_file);
    for(size_t out = 0; out < test_mat.size(); out++){
        const int u = test_mat[out].first;
        const int i = test_mat[out].second;
        wp << P.col(u).dot(Q.col(i)) << endl;
    }
    wp.close();

    return 0;
}
