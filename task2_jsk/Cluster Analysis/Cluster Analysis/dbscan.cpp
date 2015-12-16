#include <fstream>
#include <queue>
#include <vector>
#include <algorithm>
#include "head.h"
#include "dbscan.h"

using namespace std;

void dbscan_clustering(Point data[], int data_size, double eps, int minPts, bool for_test)
{
	Status *data_status = new Status[data_size];
	int i;
	int j;
	int k;
	int count;
	int cluster_num = 0;
	double **dist = new double*[data_size];
	char file_name[100];
	ofstream outFile;

	for (i = 0; i < data_size; ++i)
	{
		data_status[i] = UNVISITED;
		dist[i] = new double[data_size];
		for (j = 0; j < data_size; ++j)
		{
			if (j < i)
			{
				dist[i][j] = dist[j][i];
			}
			else if (j == i)
			{
				dist[i][j] = 0;
			}
			else
			{
				dist[i][j] = sqrt((data[i].x - data[j].x) * (data[i].x - data[j].x) + (data[i].y - data[j].y) * (data[i].y - data[j].y));
			}
		}
	}

	for (i = 0; i < data_size; ++i)
	{
		queue<int> neighbour;
		if (data_status[i] == UNVISITED)
		{
			for (j = 0, count = 0; j < data_size; ++j)
			{
				if (dist[i][j] < eps)
				{
					++count;
					if (j != i && data_status[j] != CLUSTER)
					{
						neighbour.push(j);
					}
				}
			}
			if (count < minPts)
			{
				data_status[i] = NOISE;
			}
			else
			{
				vector<int> cluster;
				cluster.push_back(i);
				data_status[i] = CLUSTER;
				while (!neighbour.empty())
				{
					j = neighbour.front();
					neighbour.pop();
					if (data_status[j] == UNVISITED)
					{
						for (k = 0, count = 0; k < data_size; ++k)
						{
							if (dist[j][k] < eps)
							{
								++count;
							}
						}
						if (count >= minPts)
						{
							for (k = 0; k < data_size; ++k)
							{
								if (dist[j][k] < eps && k != j && data_status[k] != CLUSTER)
								{
									neighbour.push(k);
								}
							}
						}
					}
					if (data_status[j] != CLUSTER)
					{
						cluster.push_back(j);
					}
					data_status[j] = CLUSTER;
				}

				if (!for_test)
				{
					sort(cluster.begin(), cluster.end());
					sprintf(file_name, "clusters\\dataset%d\\dbscan\\%.1f\\%d\\%d.dat", (data_size == SIZE2) + 1, eps, minPts, cluster_num);
					outFile.open(file_name, ios::out);
					for (j = 0, count = cluster.size(); j < count; ++j)
					{
						outFile<<cluster[j];
						if (j < count - 1)
						{
							outFile<<endl;
						}
					}
					outFile.close();
				}
				++cluster_num;
			}
		}
	}

	delete [] data_status;
	for (i = 0; i < data_size; ++i)
	{
		delete [] dist[i];
	}
	delete [] dist;
}

void dbscan(Point data[], int data_size, const double para_eps[], const int para_minPts[])
{
	int i;
	int j;
	char cmd[100];

	for (i = 0; i < PNUM; ++i)
	{
		for (j = 0; j < PNUM; ++j)
		{
			sprintf(cmd, "del clusters\\dataset%d\\dbscan\\%.1f\\%d\\*.dat", (data_size == SIZE2) + 1, para_eps[i], para_minPts[j]);
			system(cmd);
			dbscan_clustering(data, data_size, para_eps[i], para_minPts[j], false);
		}
	}
}