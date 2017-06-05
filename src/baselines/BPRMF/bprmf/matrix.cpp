#include "matrix.h"
#include "util.h"


vector<UIpair> read_oneclass_matrix(const char *file_name, Parameter &param){
    ifstream f_in(file_name);
    if (!f_in.good()) {
        ERR_EXIT("Open error: %s", file_name);
    }
    vector<UIpair> mat;
    int uu, ii;
    while( f_in >> uu >> ii ){
        mat.push_back( make_pair(uu, ii) );
        param.numU = max(param.numU, uu+1);
        param.numI = max(param.numI, ii+1);
    }
    return mat;
}

void linear_normalize(Matrix &mat) {
    Matrix::Scalar min_value = mat.maxCoeff();
    Matrix::Scalar max_value = mat.minCoeff();

    //FIXME: assert min_value != max_value
#pragma omp parallel for collapse(2)
    for (int j = 0; j < mat.cols(); j++) {
        for (int i = 0; i < mat.rows(); i++) {
            mat(i, j) = (mat(i, j) - min_value) / (max_value - min_value);
        }
    }
}

void meanvar_normalize(Matrix &mat){

    double mean = 0.0, var = 0.0;
    
//#pragma omp parallel for collapse(2) reduction(+:mean)
    for (int j = 0; j < mat.cols(); j++) {
        for(int i = 0; i < mat.rows(); i++) {
            mean += mat(i, j);
        }
    }
    mean /= (double)( mat.rows() * mat.cols() );
    
//#pragma omp parallel for collapse(2) reduction(+:var)
    for (int j = 0; j < mat.cols(); j++) {
        for(int i = 0; i < mat.rows(); i++) {
            var += pow((mat(i, j) - mean), 2);
        }
    }
    var = sqrt(var/ (double)(mat.cols() * mat.rows()));
    
#pragma omp parallel for collapse(2)
    for (int j = 0; j < mat.cols(); j++) {
        for(int i = 0; i < mat.rows(); i++) {
            mat(i, j) = (mat(i, j) - mean) / var;
        }
    }

}

