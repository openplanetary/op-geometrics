
# coding: utf-8

# In[ ]:


import ads
import json
import requests
import re
import io
import pandas as pd
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


json_name = "features.json"
features = []


# In[ ]:


with open(json_name) as fin:
    features = parse_json_stream(fin.read())


# In[ ]:


# write a json file with extended list of publications for each feature
# publications are requested from ADS API
# list of features is stored in features variable
with io.open('features_extended.json', 'w', encoding='utf-8') as fout:
    for feature in features:
        print(feature.name)
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
        #write extended feature info to a new json file
        fout.write(str(json.dumps(feature.dump(), ensure_ascii=False, indent=4))+"\n")
fout.close()


# In[ ]:


pd.set_option('display.max_colwidth', -1)
df = pd.DataFrame([feature.to_dict() for feature in features])


# In[ ]:


#print(df["publications"][0])


# In[ ]:




