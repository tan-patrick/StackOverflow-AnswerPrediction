#pragma once



pair<Matrix, Matrix> bprmf(const vector<UIpair> &train_mat,
                           const vector<UIpair> &valid_mat,
                           const Parameter &param);


void write_brpmf(const char filename[],
                 const Matrix &P,
                 const Matrix &Q,
                 const Parameter &param);

pair<Matrix, Matrix> read_bprmf(const char filename[],
                                const Parameter &param);

double calc_auc_with_data(const vector<UIpair> &train,
                          const vector<UIpair> &valid,
                          const Matrix &P,
                          const Matrix &Q,
                          const Parameter &param);
