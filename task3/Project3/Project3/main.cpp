#include <iostream>
#include <fstream>
#include <map>
#include "dbscan.h"
#include "bi_kmeans.h"

using namespace std;

#define LOCATION_EPS 0.5
#define LOCATION_MINPTS 10
#define USER_K 100
#define OUTPUT_CNUM 5

void location_clustering()
{
	int i;
	int data_size;
	int user;
	__int64 moment;
	Location coordinate;
	Location *data;
	map<int, Location> data_map;
	map<int, Location>::iterator it;
	ifstream inFile("result.txt", ios::in);

	if (inFile.fail())
	{
		cout<<"The file result.txt does not exist!"<<endl;
		return;
	}
	while (!inFile.eof())
	{
		inFile>>user>>moment>>coordinate.latitude>>coordinate.longitude>>coordinate.location;
		data_map[coordinate.location] = coordinate;
	}
	inFile.close();

	data_size = data_map.size();
	data = new Location[data_size];
	for (i = 0, it = data_map.begin(); i < data_size; ++i, ++it)
	{
		data[i] = it->second;
	}
	dbscan_clustering(data, data_size, LOCATION_EPS, LOCATION_MINPTS);

	delete [] data;
}

void user_coord_gen()
{
	int i;
	int j;
	int size;
	Location centroid;
	User record;
	User max_value;
	User min_value;
	map<int, Location> location_map;
	map<int, Location>::iterator location_it;
	map<int, User> user_map;
	map<int, User>::iterator user_it;
	ifstream inFile("location-coord.txt", ios::in);
	ofstream outFile("user-coord.txt", ios::out);

	if (inFile.fail())
	{
		location_clustering();
		inFile.open("location-coord.txt", ios::in);
	}
	while (!inFile.eof())
	{
		inFile>>size;
		if (size == 0)
		{
			break;
		}
		inFile>>centroid.latitude>>centroid.longitude;
		for (i = 0; i < size; ++i)
		{
			inFile>>j;
			location_map[j] = centroid;
		}
	}
	inFile.close();

	inFile.open("result.txt", ios::in);
	if (inFile.fail())
	{
		cout<<"The file result.txt does not exist!"<<endl;
		return;
	}
	while (!inFile.eof())
	{
		inFile>>record.user>>record.time_ave>>record.latitude_ave>>record.longitude_ave>>record.count;
		location_it = location_map.find(record.count);
		if (location_it != location_map.end())
		{
			record.latitude_ave = location_it->second.latitude;
			record.longitude_ave = location_it->second.longitude;
			user_it = user_map.find(record.user);
			if (user_it != user_map.end())
			{
				user_it->second.time_ave += record.time_ave;
				user_it->second.time_var += record.time_ave * record.time_ave;
				user_it->second.latitude_ave += record.latitude_ave;
				user_it->second.latitude_var += record.latitude_ave * record.latitude_ave;
				user_it->second.longitude_ave += record.longitude_ave;
				user_it->second.longitude_var += record.longitude_ave * record.longitude_ave;
				++(user_it->second.count);
			}
			else
			{
				record.time_var = record.time_ave * record.time_ave;
				record.latitude_var = record.latitude_ave * record.latitude_ave;
				record.longitude_var = record.longitude_ave * record.longitude_ave;
				record.count = 1;
				user_map.insert(make_pair(record.user, record));
			}
		}
	}
	inFile.close();

	max_value.time_ave = -DBL_MAX;
	max_value.time_var = -DBL_MAX;
	max_value.latitude_ave = -DBL_MAX;
	max_value.latitude_var = -DBL_MAX;
	max_value.longitude_ave = -DBL_MAX;
	max_value.longitude_var = -DBL_MAX;
	min_value.time_ave = DBL_MAX;
	min_value.time_var = DBL_MAX;
	min_value.latitude_ave = DBL_MAX;
	min_value.latitude_var = DBL_MAX;
	min_value.longitude_ave = DBL_MAX;
	min_value.longitude_var = DBL_MAX;
	for (user_it = user_map.begin(); user_it != user_map.end(); ++user_it)
	{
		user_it->second.time_ave /= user_it->second.count;
		if (user_it->second.time_ave < min_value.time_ave)
		{
			min_value.time_ave = user_it->second.time_ave;
		}
		if (user_it->second.time_ave > max_value.time_ave)
		{
			max_value.time_ave = user_it->second.time_ave;
		}

		user_it->second.time_var = user_it->second.time_var / user_it->second.count - user_it->second.time_ave * user_it->second.time_ave;
		if (user_it->second.time_var < min_value.time_var)
		{
			min_value.time_var = user_it->second.time_var;
		}
		if (user_it->second.time_var > max_value.time_var)
		{
			max_value.time_var = user_it->second.time_var;
		}

		user_it->second.latitude_ave /= user_it->second.count;
		if (user_it->second.latitude_ave < min_value.latitude_ave)
		{
			min_value.latitude_ave = user_it->second.latitude_ave;
		}
		if (user_it->second.latitude_ave > max_value.latitude_ave)
		{
			max_value.latitude_ave = user_it->second.latitude_ave;
		}

		user_it->second.latitude_var = user_it->second.latitude_var / user_it->second.count - user_it->second.latitude_ave * user_it->second.latitude_ave;
		if (user_it->second.latitude_var < min_value.latitude_var)
		{
			min_value.latitude_var = user_it->second.latitude_var;
		}
		if (user_it->second.latitude_var > max_value.latitude_var)
		{
			max_value.latitude_var = user_it->second.latitude_var;
		}

		user_it->second.longitude_ave /= user_it->second.count;
		if (user_it->second.longitude_ave < min_value.longitude_ave)
		{
			min_value.longitude_ave = user_it->second.longitude_ave;
		}
		if (user_it->second.longitude_ave > max_value.longitude_ave)
		{
			max_value.longitude_ave = user_it->second.longitude_ave;
		}

		user_it->second.longitude_var = user_it->second.longitude_var / user_it->second.count - user_it->second.longitude_ave * user_it->second.longitude_ave;
		if (user_it->second.longitude_var < min_value.longitude_var)
		{
			min_value.longitude_var = user_it->second.longitude_var;
		}
		if (user_it->second.longitude_var > max_value.longitude_var)
		{
			max_value.longitude_var = user_it->second.longitude_var;
		}
	}

	size = user_map.size();
	outFile<<size<<endl;
	for (user_it = user_map.begin(); user_it != user_map.end(); ++user_it)
	{
		if (max_value.time_ave > min_value.time_ave)
		{
			user_it->second.time_ave = (user_it->second.time_ave - min_value.time_ave) / (max_value.time_ave - min_value.time_ave);
		}
		if (max_value.time_var > min_value.time_var)
		{
			user_it->second.time_var = (user_it->second.time_var - min_value.time_var) / (max_value.time_var - min_value.time_var);
		}
		if (max_value.latitude_ave > min_value.latitude_ave)
		{
			user_it->second.latitude_ave = (user_it->second.latitude_ave - min_value.latitude_ave) / (max_value.latitude_ave - min_value.latitude_ave);
		}
		if (max_value.latitude_var > min_value.latitude_var)
		{
			user_it->second.latitude_var = (user_it->second.latitude_var - min_value.latitude_var) / (max_value.latitude_var - min_value.latitude_var);
		}
		if (max_value.longitude_ave > min_value.longitude_ave)
		{
			user_it->second.longitude_ave = (user_it->second.longitude_ave - min_value.longitude_ave) / (max_value.longitude_ave - min_value.longitude_ave);
		}
		if (max_value.longitude_var > min_value.longitude_var)
		{
			user_it->second.longitude_var = (user_it->second.longitude_var - min_value.longitude_var) / (max_value.longitude_var - min_value.longitude_var);
		}

		outFile<<user_it->second.user<<'\t'<<user_it->second.time_ave<<'\t'<<user_it->second.time_var<<'\t'<<user_it->second.latitude_ave<<'\t'<<
				 user_it->second.latitude_var<<'\t'<<user_it->second.longitude_ave<<'\t'<<user_it->second.longitude_var<<endl;
	}
	outFile.close();
}

void user_clustering()
{
	int i;
	int data_size;
	User *data;
	ifstream inFile("user-coord.txt", ios::in);

	if (inFile.fail())
	{
		user_coord_gen();
		inFile.open("user-coord.txt", ios::in);
	}
	inFile>>data_size;
	data = new User[data_size];
	for (i = 0; i < data_size; ++i)
	{
		inFile>>data[i].user>>data[i].time_ave>>data[i].time_var>>data[i].latitude_ave>>data[i].latitude_var>>data[i].longitude_ave>>data[i].longitude_var;
	}
	inFile.close();
	bi_kmeans_clustering(data, data_size, USER_K, OUTPUT_CNUM);

	delete [] data;
}

void main()
{
	user_clustering();
}