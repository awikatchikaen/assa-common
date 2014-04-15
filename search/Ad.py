'''
Created on 1 avr. 2014

@author: fcs
'''

class Ad(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.title=""
        self.price=""
        self.desc=""
        self.nom=""
        self.link=""
        self.lstImages=[]
        self.location=""
        self.date=""
        
    def __str__(self):
        #txt="\r\n"+self.title
        txt=self.title
        #txt+="\r\n \--> texte de recherche : "+str(self.textRecherche)
        return txt