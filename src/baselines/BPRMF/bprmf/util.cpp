#include "util.h"
#include <unistd.h>
#include <getopt.h>


void exit_with_predict_usage(){
	printf(
	"Usage: bprmf-predict [options] train model test [predict_file]\n"
	"options:\n"
    "  -q quiet mode\n"
    "file_format:\n"
    "  uid iid\n"
	);
    exit(1);
}


void exit_with_usage(){
    Parameter p;
	printf(
	"Usage: bprmf [options] train_matrix valid_matrix [model_file]\n"
	"options:\n"
    "  -K latent size (default %d)\n"
	"  -L learning rate (default %e)\n"
	"  -U #(User)\n"
	"  -I #(Item)\n"
	"  -u user regularization (default %e)\n"
	"  -i item regularization (default %e)\n"
	"  -s number of negative samples for each postive sample (default %d)\n"
    "  -S validation AUC calculation (0-actual, 1-sample, default %d)\n"
    "  -n matrix initial normalization (0-None, 1-Linear, 2-MeanVar, default %d)\n"
    "  -r random seed (default %d)\n"
    "  -q quiet mode\n"
    "file_format:\n"
    "  uid iid\n", p.K, p.learning_rate, p.reg_user, p.reg_item, p.nSample, p.vAUC, p.norm, p.random_seed
	);
    exit(1);
}


int read_predict_parameter(int argc, const char* argv[], Parameter &param){
    int opt;
    while( (opt = getopt(argc, (char**) argv, "q")) != -1 ){
		switch(opt) {
			case 'q':
                param.quiet = true;
                break;
            case '?':
                fprintf(stderr, "Illegal option:-%c\n", isprint(optopt)?optopt:'#');
                exit_with_predict_usage();
                break;
			default:
                exit_with_predict_usage();
                break;
        }
    }
    return optind;
}


int read_parameter(const int argc, const char* argv[], Parameter &param){
    int i = 1;
    int opt;
    while( (opt = getopt(argc, (char**) argv, "K:L:U:I:s:u:i:n:r:S:q")) != -1 ){
		switch(opt) {
			case 'K':
				param.K = atoi(optarg);
				break;
            case 'L':
                param.learning_rate = atof(optarg);
                break;
            case 'U':
                param.numU = atoi(optarg);
                break;
            case 'I':
                param.numI = atoi(optarg);
                break;
            case 's':
                param.nSample = atoi(optarg);
                break;
            case 'u':
                param.reg_user = atof(optarg);
                break;
            case 'i':
                param.reg_item = atof(optarg);
                break;
            case 'n':
                param.norm = atoi(optarg);
                break;
            case 'r':
                param.random_seed = atoi(optarg);
                break;
            case 'S':
                param.vAUC = atoi(optarg);
                break;
            case 'q':
                param.quiet = true;
                --i;
                break;
            case '?':
                exit_with_usage();
                break;
			default:
                exit_with_usage();
                break;
        }

    }
    return optind;
}


void set_rand_seed(int seed) {
    srand(seed);
    //srand(time(NULL));
}
