#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <time.h>
#include "bi_kmeans.h"

using namespace std;

inline bool equal_user(User &u1, User &u2)
{
	if (u1.time_ave == u2.time_ave && u1.time_var == u2.time_var && u1.latitude_ave == u2.latitude_ave &&
		u1.latitude_var == u2.latitude_var && u1.longitude_ave == u2.longitude_ave && u1.longitude_var == u2.longitude_var)
	{
		return true;
	}
	else
	{
		return false;
	}
}

inline double square_dist(User &u1, User &u2)
{
	return (u1.time_ave - u2.time_ave) * (u1.time_ave - u2.time_ave) + (u1.time_var - u2.time_var) * (u1.time_var - u2.time_var) +
		   (u1.latitude_ave - u2.latitude_ave) * (u1.latitude_ave - u2.latitude_ave) + (u1.latitude_var - u2.latitude_var) * (u1.latitude_var - u2.latitude_var) +
		   (u1.longitude_ave - u2.longitude_ave) * (u1.longitude_ave - u2.longitude_ave) + (u1.longitude_var - u2.longitude_var) * (u1.longitude_var - u2.longitude_var);
}

void bi_kmeans_clustering(User data[], int data_size, int K, int output_cnum)
{
	int j;
	int k;
	int l;
	int size;
	int label;
	int cur_cnum = 1;
	double SSE;
	double lowest_SSE;
	double save_SSE[2];
	double *ave_SSE = new double[K];
	char file_name[100];
	ofstream outFile;
	User old_centroids[2];
	User new_centroids[2];
	vector<int> temp[2];
	vector<int> best[2];
	vector<int> *cluster = new vector<int>[K];
	multimap<double, int> sort_clusters;
	multimap<double, int>::iterator it;

	for (j = 0; j < K; ++j)
	{
		ave_SSE[j] = 0;
	}
	cluster[0].reserve(data_size);
	for (j = 0; j < data_size; ++j)
	{
		cluster[0].push_back(j);
	}

	while (cur_cnum < K)
	{
		size = cluster[0].size();
		label = 0;
		for (j = 1; j < cur_cnum; ++j)
		{
			if (cluster[j].size() > size)
			{
				size = cluster[j].size();
				label = j;
			}
		}

		lowest_SSE = DBL_MAX;
		size = cluster[label].size();
		for (j = 0; j < ITER_TIMES; ++j)
		{
			srand((unsigned)time(NULL));
			new_centroids[0] = data[cluster[label][rand() % size]];
			do 
			{
				new_centroids[1] = data[cluster[label][rand() % size]];
			} while (equal_user(new_centroids[1], new_centroids[0]));

			do 
			{
				for (k = 0; k < 2; ++k)
				{
					old_centroids[k] = new_centroids[k];
					new_centroids[k].time_ave = 0;
					new_centroids[k].time_var = 0;
					new_centroids[k].latitude_ave = 0;
					new_centroids[k].latitude_var = 0;
					new_centroids[k].longitude_ave = 0;
					new_centroids[k].longitude_var = 0;
					temp[k].clear();
				}

				for (k = 0; k < size; ++k)
				{
					if (square_dist(data[cluster[label][k]], old_centroids[0]) < square_dist(data[cluster[label][k]], old_centroids[1]))
					{
						temp[0].push_back(cluster[label][k]);
					}
					else
					{
						temp[1].push_back(cluster[label][k]);
					}
				}
				for (k = 0; k < 2; ++k)
				{
					for (l = 0; l < temp[k].size(); ++l)
					{
						new_centroids[k].time_ave += data[temp[k][l]].time_ave;
						new_centroids[k].time_var += data[temp[k][l]].time_var;
						new_centroids[k].latitude_ave += data[temp[k][l]].latitude_ave;
						new_centroids[k].latitude_var += data[temp[k][l]].latitude_var;
						new_centroids[k].longitude_ave += data[temp[k][l]].longitude_ave;
						new_centroids[k].longitude_var += data[temp[k][l]].longitude_var;
					}
					new_centroids[k].time_ave /= temp[k].size();
					new_centroids[k].time_var /= temp[k].size();
					new_centroids[k].latitude_ave /= temp[k].size();
					new_centroids[k].latitude_var /= temp[k].size();
					new_centroids[k].longitude_ave /= temp[k].size();
					new_centroids[k].longitude_var /= temp[k].size();
				}
			} while (!(equal_user(new_centroids[0], old_centroids[0]) && equal_user(new_centroids[1], old_centroids[1])));

			SSE = 0;
			for (k = 0; k < 2; ++k)
			{
				for (l = 0; l < temp[k].size(); ++l)
				{
					SSE += square_dist(data[temp[k][l]], new_centroids[k]);
				}
				if (k == 0)
				{
					save_SSE[0] = SSE;
				}
				else
				{
					save_SSE[1] = SSE - save_SSE[0];
				}
			}
			if (SSE < lowest_SSE)
			{
				lowest_SSE = SSE;
				ave_SSE[label] = save_SSE[0] / temp[0].size();
				ave_SSE[cur_cnum] = save_SSE[1] / temp[1].size();
				for (k = 0; k < 2; ++k)
				{
					best[k].swap(temp[k]);
				}
			}
		}

		cluster[label].swap(best[0]);
		cluster[cur_cnum].swap(best[1]);
		cout<<++cur_cnum<<endl;
	}

	for (j = 0; j < K; ++j)
	{
		sort_clusters.insert(make_pair(ave_SSE[j], j));
	}
	for (j = 0, it = sort_clusters.begin(); j < output_cnum; ++it)
	{
		size = cluster[it->second].size();
		if (size < 2)
		{
			continue;
		}
		sprintf(file_name, "user_clusters\\%d.txt", j);
		outFile.open(file_name, ios::out);
		for (k = 0; k < size; ++k)
		{
			outFile<<data[cluster[it->second][k]].user;
			if (k < size - 1)
			{
				outFile<<endl;
			}
		}
		outFile.close();
		++j;
	}

	delete [] ave_SSE;
	delete [] cluster;
}