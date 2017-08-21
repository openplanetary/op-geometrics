# name_pol_ddbb

## Brief
Python script to create a gazetteer (represented as a JSON file) of Mars features. Data have to be provided in a csv file (e.g. 'Mars.csv'). 

## How to run the script

Python3 version should be used. Jupyter notebook ipynb-file is also provided for convenience.

```shell 
python database_merged.py [file_name.csv] [database_outfile.json]
```
The names of input csv and output json files are optional, if not provided, 'Mars_short.csv' and 'features.json' are taken respectively.

## Dependencies

The following additional modules should be pre-installed:

```
bs4, requests, gdal, pandas, json and ADS
```
For successful installation of ADS API Python package please follow the steps described in the website <http://ads.readthedocs.io/en/latest/#getting-started> .

In case you are using jupyter-notebook it is easier to get all other packages with conda, e.g.

```shell
conda install gdal
```

## Example

Example script 'database_ads_querying_ex' is provided as a jupyter-notebook and a python script. Script creates a database and makes queries to ADS API. By altering script variables it is possible to build new databases and create particular requests for publications related to a particular toponym. 

```shell
python database_ads_querying_ex.py
```

