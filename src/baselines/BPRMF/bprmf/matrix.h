#pragma once

#include <fstream>
#include <vector>
#include <algorithm>
#include <Eigen/Sparse>
#include "error.h"
#include "util.h"
using namespace std;


typedef Eigen::ArrayXd Array;
typedef Eigen::MatrixXd Matrix;
typedef Eigen::VectorXd Vector;
typedef Eigen::SparseMatrix<double> SparseMatrix;
typedef pair<int,int> UIpair;

vector<UIpair> read_oneclass_matrix(const char *file_name, Parameter &param);

void linear_normalize(Matrix&);
void meanvar_normalize(Matrix &mat);
