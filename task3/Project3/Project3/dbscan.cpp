#include <fstream>
#include <queue>
#include <vector>
#include "dbscan.h"

using namespace std;

void dbscan_clustering(Location data[], int location_size, double eps, int minPts)
{
	Status *data_status = new Status[location_size];
	int i;
	int j;
	int k;
	int count;
	double sum_latitude;
	double sum_longitude;
	double **dist = new double*[location_size];
	ofstream outFile("location-coord.txt", ios::out);

	for (i = 0; i < location_size; ++i)
	{
		data_status[i] = UNVISITED;
		dist[i] = new double[location_size];
		for (j = 0; j < location_size; ++j)
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
				dist[i][j] = sqrt((data[i].latitude - data[j].latitude) * (data[i].latitude - data[j].latitude) +
								  (data[i].longitude - data[j].longitude) * (data[i].longitude - data[j].longitude));
			}
		}
	}

	for (i = 0; i < location_size; ++i)
	{
		queue<int> neighbour;
		if (data_status[i] == UNVISITED)
		{
			for (j = 0, count = 0; j < location_size; ++j)
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
						for (k = 0, count = 0; k < location_size; ++k)
						{
							if (dist[j][k] < eps)
							{
								++count;
							}
						}
						if (count >= minPts)
						{
							for (k = 0; k < location_size; ++k)
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

				count = cluster.size();
				outFile<<count<<endl;
				for (j = 0, sum_latitude = 0, sum_longitude = 0; j < count; ++j)
				{
					sum_latitude += data[cluster[j]].latitude;
					sum_longitude += data[cluster[j]].longitude;
				}
				outFile<<sum_latitude / count<<'\t'<<sum_longitude / count<<endl;
				for (j = 0; j < count; ++j)
				{
					outFile<<data[cluster[j]].location<<endl;
				}
			}
		}
	}

	outFile<<0;
	outFile.close();
	delete [] data_status;
	for (i = 0; i < location_size; ++i)
	{
		delete [] dist[i];
	}
	delete [] dist;
}