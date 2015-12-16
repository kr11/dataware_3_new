#ifndef BI_KMEANS_H
#define BI_KMEANS_H

#define KNUM 5
#define ITER_TIMES 10
#define KMEANS_MAX_CNUM 19

const int para1_k[KNUM] = {11, 13, 15, 17, 19};
const int para2_k[KNUM] = {5, 6, 7, 8, 9};

void bi_kmeans_clustering(Point data[], int data_size, const int para_k[], int knum, bool for_test);

#endif