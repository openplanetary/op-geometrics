
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
import re
import ogr
import json
import csv
import io


# In[ ]:


# an encapsulation of data retrieved about a geographical feature
# an element of a Gazetteer 
class Feature:
    def __init__(self, fname, fid, fcoord, fpubl):
        self.name = fname
        self.id = fid
        self.pcoord = fcoord
        self.publ = fpubl
    # in case # publications for a feature > 1
    def addPublications(self, nEntry):
        self.publ.append(nEntry)
    # writing routine to a json file
    def dump(self):
        return {"Feature " + self.name : {'id': self.id,
                               'polygon_coordinates': self.pcoord,
                               'publications': self.publ}}


# In[ ]:


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
        coord_end = re.search('\)+', new_data)
        #compose a string with found pattern and coordinates in brackets
        geomStr = text.group() + new_data[:coord_end.start()] + coord_end.group()
    except AttributeError:
        print (searchPattern + ' pattern is not found!!')
        geomStr = 'NONE'
    return geomStr


# In[ ]:


#url path for retriving data for each feature
#the name of the feature should be appended
url = "https://planetarynames.wr.usgs.gov/Feature/"


# In[ ]:


# no headers should be present in a csv file
# the first two values must be featureID and feature_name
# JSON file is written with utf8 due to unicode standard of publications
with open('Mars.csv', mode='r') as fin, io.open('features.json', 'w', encoding='utf-8') as fout:
    reader = csv.reader(fin, delimiter=',')
    for rows in reader:
        if (len(rows) > 1):
            featId = rows[0]
            featName = rows[1].strip("[]")
            furl = url + featId
            print(furl)
            print(featName)
            req = requests.get(furl)
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
            geomOGR = ogr.CreateGeometryFromWkt(geomStr)
            
            #search for publications with html tree 
            #in the given html th tag contained td child td with publication name 
            res = data.find("th", text="Reference").find_next_sibling("td").text
            #print(res.strip())
            
            nFeat = Feature(featName, featId, geomStr, res.strip())
            # write feature to a gazetteer represented by a JSON file
            #json.dump(nFeat.dump(), fout, ensure_ascii=False, indent=4)
            fout.write(str(json.dumps(nFeat.dump(), ensure_ascii=False, indent=4)))
fout.close()


# In[ ]:




