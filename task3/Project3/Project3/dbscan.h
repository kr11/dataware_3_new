#ifndef DBSCAN_H
#define DBSCAN_H

enum Status {UNVISITED, CLUSTER, NOISE};

struct Location
{
	int location;
	double latitude;
	double longitude;
};

void dbscan_clustering(Location data[], int location_size, double eps, int minPts);

#endif