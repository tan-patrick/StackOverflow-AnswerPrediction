#include <cmath>
#include <set>
#include <algorithm>
#include "matrix.h"
#include "util.h"

#define MAX_ITER 500

void write_brpmf(const char filename[],
                 const Matrix &P,
                 const Matrix &Q,
                 const Parameter &param){
    ofstream wp(filename, ios::binary);
    
    // write parameter info
    wp.write((char*) &param.numU, sizeof(int));
    wp.write((char*) &param.numI, sizeof(int));
    wp.write((char*) &param.K, sizeof(int));
    
    // write matrix P
    wp.write((char*) &P(0,0), sizeof(Matrix::Scalar) * P.rows() * P.cols());
    
    // write matrix Q
    wp.write((char*) &Q(0,0), sizeof(Matrix::Scalar) * Q.rows() * Q.cols());

    wp.close();
}

pair<Matrix, Matrix> read_bprmf(const char filename[],
                                const Parameter &param){
    ifstream fp(filename, ios::binary);
    
    // read parameter info
    fp.read((char*) &param.numU, sizeof(int));
    fp.read((char*) &param.numI, sizeof(int));
    fp.read((char*) &param.K, sizeof(int));
    
    // construct and read matrix P
    Matrix P(param.K, param.numU);
    fp.read((char*) &P(0,0), sizeof(Matrix::Scalar) * P.rows() * P.cols());
    
    // write matrix Q
    Matrix Q(param.K, param.numI);
    fp.read((char*) &Q(0,0), sizeof(Matrix::Scalar) * Q.rows() * Q.cols());
    
    fp.close();

    return make_pair(P, Q);
}


double calc_auc_sample(const vector< set<int> > &train_set,
                const vector< set<int> > &test_set,
                const Matrix &P,
                const Matrix &Q,
                const Parameter &param){

    double auc = 0.0;
#pragma omp parallel for reduction(+:auc)
    for(int u = 0; u < param.numU; ++u){
        if( test_set[u].size() == 0 ){
           auc += 1.0;
           continue;
        }
        double correct = 0.0, sum = 0.0;
        for(set<int>::iterator it = test_set[u].begin(); it != test_set[u].end(); ++it){
            int left = param.nSample;
            const int i1 = *it;
            while(left--){
                int i2 = rand() % param.numI;
                if(test_set[u].find(i2) != test_set[u].end() || train_set[u].find(i2) != train_set[u].end()){
                    ++left;
                    continue;                    
                }
                const double p1 = P.col(u).dot(Q.col(i1));
                const double p2 = P.col(u).dot(Q.col(i2));
                sum += 1.0;
                if( p1 > p2 ){
                    correct += 1.0;
                }
            }
        }
        auc += correct / sum;
    }
    auc /= (double) param.numU;
    return auc;
}


double calc_auc(const vector< set<int> > &train_set,
                const vector< set<int> > &test_set,
                const Matrix &P,
                const Matrix &Q,
                const Parameter &param){
    if(param.vAUC == 1){
        return calc_auc_sample(train_set, test_set, P, Q, param);
    }

    double auc = 0.0;

    //    Matrix R = P.transpose().eval() * Q;
#pragma omp parallel for reduction(+:auc)
    for(int u = 0; u < param.numU; ++u){
        if( test_set[u].size() == 0 ){
           auc += 1.0;
           continue;
        }

        int num_test = 0;
        vector< pair<double, bool> > plist;
        for(int i=0; i < param.numI; ++i){
            if( test_set[u].find(i) == test_set[u].end() &&
                train_set[u].find(i) != train_set[u].end() ){
                continue;
            }
            const double p = P.col(u).dot( Q.col(i) );
            // const double p = R(u, i);
            plist.push_back( make_pair(p, (test_set[u].find(i) != test_set[u].end()) ) ); 
            ++num_test;
        }
        sort(plist.begin(), plist.end(), greater< pair<double, bool> >() );

        const int rnum = (int) test_set[u].size();
        double local_auc = 0.0, nc = 0.0;
        for(int i=0, rc = 0; i < plist.size() && rc < rnum; ++i){
            if( plist[i].second ){
                local_auc += num_test - nc - rnum;
                ++rc;
            }else{
                nc += 1.0;
            }
        }
        local_auc /= (double) rnum;
        local_auc /= (double)(num_test - rnum);

        auc += local_auc;
    }
    auc /= (double) param.numU;
    
    return auc;
}

double calc_auc_with_data(const vector<UIpair> &train,
                          const vector<UIpair> &valid,
                          const Matrix &P,
                          const Matrix &Q,
                          const Parameter &param){
    vector< set<int> > tset(param.numU);
    vector< set<int> > vset(param.numU);

    for(size_t i=0;i<train.size();i++){
        tset[ train[i].first ].insert( train[i].second );
    }
    for(size_t i=0;i<valid.size();i++){
        vset[ valid[i].first ].insert( valid[i].second );
    }
    return calc_auc(tset, vset, P, Q, param);
}


pair<Matrix, Matrix> bprmf(const vector<UIpair> &train,
                           const vector<UIpair> &valid,
                           const Parameter &param){

    vector< set<int> > empty_set(param.numU);
    vector< set<int> > tset(param.numU);
    vector< set<int> > vset(param.numU);

    for(size_t i=0;i<train.size();i++){
        tset[ train[i].first ].insert( train[i].second );
    }
    for(size_t i=0;i<valid.size();i++){
        vset[ valid[i].first ].insert( valid[i].second );
    }

    Matrix P = Matrix::Random(param.K, param.numU);
    Matrix Q = Matrix::Random(param.K, param.numI);
    if(param.norm == NORM_LINEAR){
        linear_normalize(P);   
        linear_normalize(Q);
    }else if(param.norm == NORM_MEANVAR){
        meanvar_normalize(P); 
        meanvar_normalize(Q); 
    }
   
    int iter = 0;
    double eta = param.learning_rate;
    const double xi_u = param.reg_user;
    const double xi_i = param.reg_item;

    Matrix optP = P;
    Matrix optQ = Q;
    double opt_auc = calc_auc(tset, vset, P, Q, param);// DBL_MAX;

    CERR(param, "Start training with "
        << "learning rate = " << eta << ", "
        << "valid AUC = " << opt_auc << endl);

    while( iter++ < MAX_ITER && eta > 1e-15){
        // Training Process
        for(size_t out_j=0;out_j<train.size();out_j++){
            const int u  = train[out_j].first;
            const int i1 = train[out_j].second;
            int sample_cnt = param.nSample;
            while(sample_cnt--){
                const int i2 = rand() % param.numI;
                if( tset[u].find(i2) != tset[u].end() ){
                    ++sample_cnt;
                    continue;
                }
                const double err =   P.col(u).dot(Q.col(i1)) 
                                   - P.col(u).dot(Q.col(i2));
                double sig = exp(-err) / ( 1.0 + exp(-err) );
                if(errno == ERANGE){
                    sig = 1.0;
                }
                
                const Vector P_u  = P.col(u)  - eta * ( -sig * ( Q.col(i1) - Q.col(i2) ) + xi_u * P.col(u) ) ;
                const Vector Q_i1 = Q.col(i1) - eta * ( -sig * (  P.col(u) ) + xi_i * Q.col(i1) );
                const Vector Q_i2 = Q.col(i2) - eta * ( -sig * ( -P.col(u) ) + xi_i * Q.col(i2) ); 
                P.col(u) = P_u;
                Q.col(i1) = Q_i1;
                Q.col(i2) = Q_i2;
            }
        }
        // Evaluation
        const double train_auc = calc_auc(empty_set, tset, P, Q, param);
        const double valid_auc = calc_auc(tset,      vset, P, Q, param);
        
        CERR(param, "Iter #" << iter << " "
            << "train AUC: " << train_auc << ",\t"
            << "valid AUC: " << valid_auc << ",\t");
       
        if( valid_auc > opt_auc ){
            eta = min(eta*2.0, param.learning_rate);
            CERR(param, "optimized,\t eta -> " << eta);
            opt_auc = valid_auc;
            optP = P;
            optQ = Q;
        }else{
            break;
            eta /= 2.0;
            CERR(param, "rejected,\t eta -> " << eta);
            --iter;
            P = optP;
            Q = optQ;
        }
        CERR(param, endl);
    }

    return make_pair(optP, optQ);
}

