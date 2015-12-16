#ifndef BI_KMEANS_H
#define BI_KMEANS_H

#define ITER_TIMES 10

struct User
{
	int user;
	double time_ave;
	double time_var;
	double latitude_ave;
	double latitude_var;
	double longitude_ave;
	double longitude_var;
	int count;
};

void bi_kmeans_clustering(User data[], int data_size, int K, int output_cnum);

#endif