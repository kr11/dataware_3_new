#include <fstream>
#include <vector>
#include <time.h>
#include "head.h"
#include "bi_kmeans.h"

using namespace std;

void bi_kmeans_clustering(Point data[], int data_size, const int para_k[], int knum, bool for_test)
{
	int i;
	int j;
	int k;
	int l;
	int size;
	int label;
	int cur_cnum;
	double SSE;
	double lowest_SSE;
	double save_SSE[2];
	double ave_SSE[KMEANS_MAX_CNUM] = {0};
	char file_name[100];
	ofstream outFile;
	Point old_centroids[2];
	Point new_centroids[2];
	vector<int> temp[2];
	vector<int> best[2];
	vector<int> cluster[KMEANS_MAX_CNUM];

	cluster[0].reserve(data_size);
	for (i = 0; i < data_size; ++i)
	{
		cluster[0].push_back(i);
	}
	cur_cnum = 1;

	for (i = 0; i < knum; ++i)
	{
		while (cur_cnum < para_k[i])
		{
			/*
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
			*/

			
			SSE = ave_SSE[0];
			label = 0;
			for (j = 1; j < cur_cnum; ++j)
			{
				if (ave_SSE[j] > SSE)
				{
					SSE = ave_SSE[j];
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
				} while (new_centroids[1].x == new_centroids[0].x && new_centroids[1].y == new_centroids[0].y);

				do 
				{
					for (k = 0; k < 2; ++k)
					{
						old_centroids[k] = new_centroids[k];
						new_centroids[k].x = 0;
						new_centroids[k].y = 0;
						temp[k].clear();
					}

					for (k = 0; k < size; ++k)
					{
						Point p = data[cluster[label][k]];
						if ((p.x - old_centroids[0].x) * (p.x - old_centroids[0].x) + (p.y - old_centroids[0].y) * (p.y - old_centroids[0].y) <
							(p.x - old_centroids[1].x) * (p.x - old_centroids[1].x) + (p.y - old_centroids[1].y) * (p.y - old_centroids[1].y))
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
							new_centroids[k].x += data[temp[k][l]].x;
							new_centroids[k].y += data[temp[k][l]].y;
						}
						new_centroids[k].x /= temp[k].size();
						new_centroids[k].y /= temp[k].size();
					}
				} while (!(new_centroids[0].x == old_centroids[0].x && new_centroids[0].y == old_centroids[0].y &&
					new_centroids[1].x == old_centroids[1].x && new_centroids[1].y == old_centroids[1].y));

				SSE = 0;
				for (k = 0; k < 2; ++k)
				{
					for (l = 0; l < temp[k].size(); ++l)
					{
						Point p = data[temp[k][l]];
						SSE += (p.x - new_centroids[k].x) * (p.x - new_centroids[k].x) + (p.y - new_centroids[k].y) * (p.y - new_centroids[k].y);
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
			++cur_cnum;
		}

		if (!for_test)
		{
			for (j = 0; j < cur_cnum; ++j)
			{
				sprintf(file_name, "clusters\\dataset%d\\bisecting k-means\\%d\\%d.dat", (data_size == SIZE2) + 1, para_k[i], j);
				outFile.open(file_name, ios::out);
				size = cluster[j].size();
				for (k = 0; k < size; ++k)
				{
					outFile<<cluster[j][k];
					if (k < size - 1)
					{
						outFile<<endl;
					}
				}
				outFile.close();
			}
		}
	}
}