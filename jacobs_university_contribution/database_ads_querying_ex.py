
# coding: utf-8

# In[ ]:


import subprocess as sub
import sys
import ads
import re
import json
import pandas as pd
import ogr
from matplotlib import pyplot as plt
from paper_class import Paper
from feature_class import Feature


# In[ ]:


# routine to read information from json file
# creates a Feature instance with extracted data
def feature_extract(obj):
    if '__type__' in obj and obj['__type__'] == 'Feature':
        return Feature(obj['name'], obj['id'], obj['polygon_coordinates'], obj['publications'])
    return Feature("None", 0, "None", "None")


# In[ ]:


# routine to parse json file and fetch definition of each feature
def parse_json_stream(text):
    list_idx = [m.start() for m in re.finditer('}\n', text)]
    list_objs = []
    last_index = 0
    for index in list_idx:
        new_feature = json.loads(text[last_index:index+2], object_hook=feature_extract)
        if (new_feature.name == "None"):
            break
        list_objs += [new_feature]
        last_index = index+2
    return list_objs


# In[ ]:


# code is taken from jupyter notebook 
# https://github.com/epn-vespa/vespamap17-hackathon/blob/master/vespa-mapping-jupyter-samp/SendName_to_IAUnomenclature_findPolygon_hacky.ipynb
def draw_feature_contour(feature):
    geomOGR = ogr.CreateGeometryFromWkt(feature.pcoord)
    
    plt.figure(figsize=(6,6))

    coords = json.loads(geomOGR.ExportToJson())['coordinates'][0]
    x = [i for i,j in coords[0]]
    y = [j for i,j in coords[0]]

    plt.plot(x, y, 'b')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Feature : ' + feature.name)
    plt.show()


# In[ ]:


# To create a database with features and their topological structure
# One needs to create a csv file with 
# https://planetarynames.wr.usgs.gov/nomenclature/AdvancedSearch
# and pass it to the database_creation script
# IMPORTANT: feature ID and feature name should be present in csv file


# In[ ]:


script_name = "database_merged.py"
csv_file_name = "Mars_short.csv"
output_file_name = "features.json"
try:
    ret = sub.call(' '.join(["python", script_name, csv_file_name, output_file_name]), shell = True)
    if (ret != 0):
        print("Child returned", ret, file=sys.stderr)
except OSError as e:
    print("Execution failed: ", e, file=sys.stderr)


# In[ ]:


# now database is built and we want to provide speific queries to ADS
authors = ["Tanaka, K. L.", "Kolb, E. J.", "Fortezzo, C."]
toponym = "Abalos Colles"
years = range(2003, 2008)
query_list = ["", "", ""]

if (toponym):
    query_list[0] = toponym

if (authors):
    for idx in range(len(authors) - 1):
        query_list[1] += "author:" + authors[idx] + " OR "
    query_list[1] += "author:" + authors[-1]
        
if (years):
    query_list[2] = "year:[" + str(years.start) + " TO " + str(years.stop) + "]" 

query = ' AND '.join(filter(None, query_list))


# In[ ]:


if (not query):
    raise RuntimeError("Empty query is not allowed!")
print(query)


# In[ ]:


#performing a query to ADS API
example_results = []
try:
    example_results = list(ads.SearchQuery(q=query, fl=['title', 'author', 'year', 'pub', 'bibcode']))
except (ads.exceptions.APIResponseError, ads.exceptions.SolrResponseParseError) as e:
    "Error: {}".format(e)


# In[ ]:


# representing results with custom Paper class
results_new = []
for paper in example_results:
    results_new.append(Paper(paper.title[0], paper.author, paper.year, paper.pub, paper.bibcode))


# In[ ]:


# dig the database for the requested toponym
with open(output_file_name) as fin:
    features = parse_json_stream(fin.read())


# In[ ]:


# if the entry exists - draw the toponym as a polygon
for feature in features:
    if (toponym == feature.name):
        print(toponym + " is found in the database!")
        draw_feature_contour(feature)
        break


# In[ ]:


# create pandas table
pd.set_option('display.max_colwidth', -1)
df = pd.DataFrame([paper.to_dict() for paper in results_new])


# In[ ]:


print(df)


# In[ ]:




