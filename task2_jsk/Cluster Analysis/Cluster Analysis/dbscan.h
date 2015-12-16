#ifndef DBSCAN_H
#define DBSCAN_H

#define PNUM 5

enum Status {UNVISITED, CLUSTER, NOISE};
const double para1_eps[PNUM] = {3e4, 3.5e4, 4e4, 4.5e4, 5e4};
const int para1_minPts[PNUM] = {50, 75, 100, 125, 150};
const double para2_eps[PNUM] = {0.7, 0.8, 0.9, 1.0, 1.1};
const int para2_minPts[PNUM] = {3, 4, 5, 6, 7};

void dbscan_clustering(Point data[], int data_size, double eps, int minPts, bool for_test);
void dbscan(Point data[], int data_size, const double para_eps[], const int para_minPts[]);

#endif