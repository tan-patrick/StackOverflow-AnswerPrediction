#include <fstream>
#include <iostream>
#include "error.h"
#include "matrix.h"
#include "model.h"
#include "util.h"
using namespace std;
int main(int argc,const char* argv[]){
    if( argc < 1 + 2){
        exit_with_usage();
    }    
    
    char* train_file = NULL;
    char* valid_file = NULL;
    char* model_file = NULL;
    Parameter param;

    /** Load parameters **/
    int train_idx = read_parameter(argc, argv, param);
    train_file = (char*) argv[train_idx++];
    valid_file = (char*) argv[train_idx++];
    if(train_idx!=argc){
        model_file = (char*)argv[train_idx];
    }
    assert(train_file != NULL);
    
    /** Set Random Seed **/
    set_rand_seed(param.random_seed);

    /** File Description **/
    if(model_file == NULL){
        model_file = new char[ strlen(train_file) + 10 ];
        sprintf(model_file,"%s.model",train_file);
    }

    CERR(param, "Train File = " << train_file << endl);
    CERR(param, "Valid File = " << valid_file << endl);
    CERR(param, "Model File = " << model_file << endl);

    /** Load Data **/
    CERR(param, "Load train and valid matrices...");
    vector<UIpair> train_mat = read_oneclass_matrix(train_file, param);
    vector<UIpair> valid_mat = read_oneclass_matrix(valid_file, param);
    CERR(param, "Done!" << endl);

    CERR(param, "(numU, numI, K) = ("
        << param.numU << ", "
        << param.numI << ", "
        << param.K << ")" << endl);

    /** Run Model **/
    pair<Matrix, Matrix> model = bprmf(train_mat, valid_mat, param);        
    
    /** Write Model **/
    write_brpmf(model_file, model.first, model.second, param);

    return 0;
}
