#include <iostream>
#include <fstream>
#include <windows.h>
#include "head.h"
#include "bi_kmeans.h"
#include "dbscan.h"
#include "evaluation.h"

using namespace std;

#define TEST_TIMES 10

const int paraT1_k[] = {17};
const double paraT1_eps = 4e4;
const int paraT1_minPts = 100;
const int paraT2_k[] = {9};
const double paraT2_eps = 1.1;
const int paraT2_minPts = 6;

void clustering(int data_size, const int para_k[], const double para_eps[], const int para_minPts[])
{
	int i;
	char file_name[20];
	ifstream inFile;
	Point *data = new Point[data_size];

	sprintf(file_name, "dataset%d.dat", (data_size == SIZE2) + 1);
	inFile.open(file_name, ios::in);
	if (inFile.fail())
	{
		cout<<"The file "<<file_name<<"does not exist!"<<endl;
		return;
	}
	for (i = 0; i < data_size; ++i)
	{
		inFile>>data[i].x>>data[i].y;
	}
	inFile.close();
	bi_kmeans_clustering(data, data_size, para_k, KNUM, false);
	dbscan(data, data_size, para_eps, para_minPts);

	delete [] data;
}

void test(int data_size, const int paraT_k[], const double paraT_eps, const int paraT_minPts)
{
	int i;
	char file_name[20];
	DWORD t1;
	DWORD t2;
	ifstream inFile;
	Point *data = new Point[data_size];

	sprintf(file_name, "dataset%d.dat", (data_size == SIZE2) + 1);
	inFile.open(file_name, ios::in);
	if (inFile.fail())
	{
		cout<<"The file "<<file_name<<"does not exist!"<<endl;
		return;
	}
	for (i = 0; i < data_size; ++i)
	{
		inFile>>data[i].x>>data[i].y;
	}
	inFile.close();
	
	cout<<"TEST_TIMES = "<<TEST_TIMES<<endl;
	cout<<"dataset: dataset"<<(data_size == SIZE2) + 1<<endl;
	cout<<"method: bisecting k-means (k = "<<paraT_k[0]<<"): elapsed time = ";
	t1 = GetTickCount();
	for (i = 0; i < TEST_TIMES; ++i)
	{
		bi_kmeans_clustering(data, data_size, paraT_k, 1, true);
	}
	t2 = GetTickCount();
	cout<<t2 - t1<<"ms"<<endl;
	cout<<"method: dbscan (eps = "<<paraT_eps<<", minPts = "<<paraT_minPts<<"): elapsed time = ";
	t1 = GetTickCount();
	for (i = 0; i < TEST_TIMES; ++i)
	{
		dbscan_clustering(data, data_size, paraT_eps, paraT_minPts, true);
	}
	t2 = GetTickCount();
	cout<<t2 - t1<<"ms"<<endl<<endl;

	delete [] data;
}

void main(int argc, char *argv[])
{
	if (argc == 2)
	{
		int flag = atoi(argv[1]);
		
		if (flag == 0)
		{
			test(SIZE1, paraT1_k, paraT1_eps, paraT1_minPts);
			test(SIZE2, paraT2_k, paraT2_eps, paraT2_minPts);
			return;
		}
		if (flag & 1)
		{
			clustering(SIZE1, para1_k, para1_eps, para1_minPts);
		}
		if (flag & 2)
		{
			clustering(SIZE2, para2_k, para2_eps, para2_minPts);
		}
	}
	evaluate();
}