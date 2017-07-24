#!/usr/bin/env bash

#enables passing the name of input csv file
if [ $# -ne 0 ] 
then
	file_csv=$1
else
	file_csv="Mars_short.csv"
fi

python feature_class.py 2> feature_class.log
if [ $? -ne 0 ] 
then 
	echo "****ERROR: feature_class.py failed***"
	echo "****Please see log file for more info****"
	exit 2 
fi

echo "****database_mapping.py execution started****"
python database_mapping.py $file_csv 2> database_mapping.log
if [ $? -ne 0 ] 
then 
	echo "****ERROR: database_mapping.py failed***"
	echo "****Please see log file for more info****"
	exit 2 
fi
echo "****database_mapping.py completed****"

echo ""

echo "****database_ads_publications.py execution started****"
python database_ads_publications.py 2> database_ads_publications.log
if [ $? -ne 0 ] 
then 
	echo "****ERROR: database_ads_publications.py failed***"
	echo "****Please see log file for more info****"
	exit 2
fi

echo "****database_ads_publications.py completed****"
echo ""
echo "****SUCCESS!****"
