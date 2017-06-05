#pragma once

#include <cstdio>
#include <cstdlib>

#define ERR_EXIT(str, ...) do {\
    fprintf(stderr, "Error (%s): " str "\n", __func__, ##__VA_ARGS__);\
    exit(EXIT_FAILURE);\
} while (false)

#define ASSERT(cond, ...) do {\
    if (!(cond)) ERR_EXIT(__VA_ARGS__);\
} while (false)

#define LOG(...) fprintf(stderr, __VA_ARGS__)

