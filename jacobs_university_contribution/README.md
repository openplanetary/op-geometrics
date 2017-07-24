# name_pol_ddbb

## Brief
Python script to create a gazetteer (represented as a JSON file) of Mars features. Data have to be provided in a csv file (e.g. 'Mars.csv'). 

## How to run the script

Python3 version should be used. Jupyter notebook ipynb-file is also provided for convenience.

```shell 
./run_script.sh [file_name.csv]
```
The name of input csv file is optional, if not provided 'Mars_short.csv' is taken instead.

## Dependencies

The following python modules should be pre-installed:

```
bs4, requests, gdal and json
```
In case you are using jupyter-notebook it is easier to get all packages with conda program.
