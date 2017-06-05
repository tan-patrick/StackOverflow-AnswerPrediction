CXXFLAGS+=-O2 -march=native -Wall -fopenmp -Wextra -Wconversion -std=c++0x -I../lib/
#CXXFLAGS+=-Ofast -march=native -Wall -fopenmp -Wextra -Wconversion -std=c++11 -I../lib/

.PHONY: all clean

all: bprmf bprmf-predict

bprmf: model.o matrix.o util.o
bprmf-predict: model.o matrix.o util.o

clean:
	$(RM) bprmf bprmf-predict model.o matrix.o util.o

