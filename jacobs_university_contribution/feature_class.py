
# coding: utf-8

# In[ ]:


# an encapsulation of data retrieved about a geographical feature
# an element of a Gazetteer 
class Feature:
    def __init__(self, fname, fid, fcoord, fpubl):
        self.name = fname
        self.id = fid
        self.pcoord = fcoord
        self.publ = []
        self.publ.append(''.join(fpubl))
        
    # in case # publications for a feature > 1
    def addPublications(self, nEntry):
        self.publ.extend(nEntry)
    # writing routine to a json file
    def dump(self):
        return {'__type__': type(self).__name__, 'name': self.name,
                               'id': self.id,
                               'polygon_coordinates': self.pcoord,
                               'publications': self.publ}


# In[ ]:




