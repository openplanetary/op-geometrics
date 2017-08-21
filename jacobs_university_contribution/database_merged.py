
# coding: utf-8

# In[5]:


from paper_class import Paper
from feature_class import Feature
import pandas as pd
import requests
import re
import ogr
import json
import csv
import io
import sys
import ads
from bs4 import BeautifulSoup


# In[6]:


# extracts the information about feature coordinates
# enclosed in brackets right after the first instance of a regex is found
# please note, that search finishes when such an instance is discovered
def getFeatureGeomCoordinates(searchPattern, data):
    #text.group() - found pattern    
    #text.start() - pointer before the pattern
    #text.end() - pointer after the pattern
    text=re.search(searchPattern, data.text)
    try:
        #extract the data after pattern and search for closing bracket
        new_data = data.text[text.end():]
        coord_end = re.search('\'', new_data)
        #compose a string with found pattern and coordinates in brackets
        geomStr = text.group() + new_data[:coord_end.start()]
    except AttributeError:
        print (searchPattern + ' pattern is not found!!')
        geomStr = 'NONE'
    return geomStr


# In[7]:


#url path for retriving data for each feature
#the name of the feature should be appended
url = "https://planetarynames.wr.usgs.gov/Feature/"
ogr.UseExceptions()  # Enable errors
file_csv = 'Mars_short.csv'
output_file_name = 'features.json'
features = []

if (len(sys.argv) > 2):
    file_csv = sys.argv[1]
    output_file_name = sys.argv[2]

# In[8]:


# no headers should be present in a csv file
# the first two values must be featureID and feature_name
# JSON file is written with utf8 due to unicode standard of publications
with open(file_csv, mode='r') as fin, io.open(output_file_name, 'w', encoding='utf-8') as fout:
    reader = csv.reader(fin, delimiter=',')
    for rows in reader:
        if (len(rows) > 1):
            featId = rows[0]
            featName = rows[1].strip("[]")
            furl = url + featId
            #print(furl)
            print(featName)
            try:
                req = requests.get(furl)
            except requests.exceptions.RequestException as e:
                "Error: {}".format(e)
                pass
            
            #html data
            data = BeautifulSoup(req.text, "lxml")
            
            #get the html-snippet with feature coordinates
            #regex: MULTI|POLYGON|LINESTRING searches for any of the keywords
            #in case MULTILINESTRING or MULTIPOLYGON the keyword MULTI is triggered 
            geomStr = getFeatureGeomCoordinates('MULTI|POLYGON|LINESTRING', data)
            #if no entry is found - search for POINT feature
            #in the current html version POINT was always preset as the center of a feature 
            #thus another separate search was needed
            if (geomStr == 'NONE'):
                #the first instance of POINT coordinates is retrieved
                geomStr = getFeatureGeomCoordinates('POINT', data)  
            try:
                geomOGR = ogr.CreateGeometryFromWkt(geomStr)
            except RuntimeError as e:
                print(e)
                pass
            
            #search for publications with html tree 
            #in the given html th tag contained td child td with publication name 
            #res = data.find("th", text="Reference").find_next_sibling("td").text
            
            feature = Feature(featName, featId, geomStr)
            # request ADS API for publications based on feature name
            # store objects of type Article
            papers = []
            try:
                papers = list(ads.SearchQuery(q=feature.name, fl=['title', 'author', 'year', 'pub', 'bibcode']))
            except (ads.exceptions.APIResponseError, ads.exceptions.SolrResponseParseError) as e:
                "Error: {}".format(e)
                continue

            citation_str = []
            # extract several fields from each publication
            # whole list of fields can be found in https://github.com/adsabs/adsabs-dev-api/blob/master/search.md#fields
            for paper in papers:
                if (not paper.title):
                    p_title = "Unknown title"
                else:    
                    p_title = paper.title[0]
                
                if (type(paper.pub).__name__ == "NoneType"):
                    p_pub = "Unknown publication"
                else:
                    p_pub = paper.pub
                p = Paper(p_title, paper.author, paper.year, p_pub, paper.bibcode)
                citation_str.append(p)
            # extend feature's list of publications 
            feature.addPublications(citation_str)
            features.append(feature)
            #write extended feature info to a new json file
            fout.write(str(json.dumps(feature.dump(), ensure_ascii=False, indent=4))+"\n")
fout.close()


# In[ ]:


pd.set_option('display.max_colwidth', -1)
df = pd.DataFrame([feature.to_dict() for feature in features])


# In[ ]:


#print(df["publications"][0])


# In[ ]:




