
# coding: utf-8

# In[ ]:


import ads
import json
import requests
import re
import io
from feature_class import Feature


# In[ ]:


def feature_extract(obj):
        if '__type__' in obj and obj['__type__'] == 'Feature':
            return Feature(obj['name'], obj['id'], obj['polygon_coordinates'], obj['publications'])
        return Feature("None", 0, "None", "None")


# In[ ]:


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


with io.open('features_short.json', 'w', encoding='utf-8') as fout:
    for feature in features:
        print(feature.name + " extended")
        try:
            papers = list(ads.SearchQuery(q=feature.name, sort="year", fl=['title', 'first_author', 'year', 'pub', 'bibcode']))
        except (ads.exceptions.APIResponseError, ads.exceptions.SolrResponseParseError) as e:
            "Error: {}".format(e)
            pass
        
        citation_str = []
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
                #print(paper.pub)
                p_pub = " : " + paper.pub + ", "
            citation_str.append(p_title + " by " + p_author + p_pub + p_year)
        feature.addPublications(citation_str)
        fout.write(str(json.dumps(feature.dump(), ensure_ascii=False, indent=4))+"\n")
fout.close()


# In[ ]:




