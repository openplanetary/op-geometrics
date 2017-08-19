
# coding: utf-8

# In[4]:


import json


# In[8]:


# an encapsulation of Article class from ADS API

class Paper :
    def __init__(self, p_title, p_authors, p_year, p_pub, p_bibcode):
        self.title = p_title
        self.authors = p_authors
        self.year = p_year
        self.publ = p_pub
        self.bibcode = p_bibcode
    
    def __str__(self):
        if (type(self.title).__name__ == "NoneType"):
            p_title = "Unknown title"
        else:    
            p_title = self.title
                
        p_authors = ', '.join(self.authors)
        p_year = str(self.year)
            
        if (type(self.publ).__name__ == "NoneType"):
            p_pub = ", "
        else:
            p_pub = " : " + self.publ + ", "
            
        return ''.join([p_title,p_authors,p_year,p_pub])
    
    # writing routine to a json file
    def dump(self):
        return {'__type__': type(self).__name__, 'title': self.title,
                               'authors': self.authors,
                               'year' : self.year,
                               'publication': self.publ,
                               'bibcode': self.bibcode }
    def toJSON(self):
        return json.dumps(self.dump(), ensure_ascii=False, indent=4)


# In[ ]:




