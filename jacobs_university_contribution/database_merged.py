
# coding: utf-8

# In[4]:


from bs4 import BeautifulSoup
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


# In[5]:


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


# In[10]:


#url path for retriving data for each feature
#the name of the feature should be appended
url = "https://planetarynames.wr.usgs.gov/Feature/"
ogr.UseExceptions()  # Enable errors
file_csv = 'Mars_short.csv'
features = []

if (len(sys.argv) > 1):
	file_csv = sys.argv[1]


# In[12]:


# no headers should be present in a csv file
# the first two values must be featureID and feature_name
# JSON file is written with utf8 due to unicode standard of publications
with open(file_csv, mode='r') as fin, io.open('features.json', 'w', encoding='utf-8') as fout:
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
            res = data.find("th", text="Reference").find_next_sibling("td").text
            
            feature = Feature(featName, featId, geomStr, res.strip())
            # request ADS API for publications based on feature name
            # store objects of type Article
            papers = []
            try:
                papers = list(ads.SearchQuery(q=feature.name, fl=['title', 'first_author', 'year', 'pub', 'bibcode']))
            except (ads.exceptions.APIResponseError, ads.exceptions.SolrResponseParseError) as e:
                "Error: {}".format(e)
                continue

            citation_str = []
            # extract several fields from each publication
            # whole list of fields can be found in https://github.com/adsabs/adsabs-dev-api/blob/master/search.md#fields
            for paper in papers:
                if (type(paper.title).__name__ == "NoneType"):
                    p_title = "Unknown"
                else:    
                    p_title = paper.title[0]

                p_author = paper.first_author
                p_year = str(paper.year)

                if (type(paper.pub).__name__ == "NoneType"):
                    p_pub = ", "
                else:
                    p_pub = " : " + paper.pub + ", "
                # combine all fields in a comprehensible string
                citation_str.append(p_title + " by " + p_author + p_pub + p_year)
            # extend feature's list of publications 
            feature.addPublications(citation_str)
            features.append(feature)
            #write extended feature info to a new json file
            fout.write(str(json.dumps(feature.dump(), ensure_ascii=False, indent=4))+"\n")
fout.close()


# In[13]:


pd.set_option('display.max_colwidth', -1)
df = pd.DataFrame([feature.to_dict() for feature in features])


# In[16]:


#print(df["publications"][0])


# In[ ]:




