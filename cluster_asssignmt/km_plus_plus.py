# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 12:49:06 2016

@author: DEEPANSHU
"""
''' for testing
a={'100':{'a':2,'b':3,'c':4},
'200':{'e':6,'f':9,'b':2},
'300':{'c':10,'f':6},
'600':{'d':20,'b':13,'e':4}}

b={'100':{'a':2,'b':3,'c':4},
'200':{'e':6,'f':9,'b':2},
'500':{'c':10,'f':6},
'700':{'d':20,'b':13,'e':4}}
'''
N=1200
def getNeighbors(dataset,vector,k):
    pass
def KMeans(dataset,initial_clusters,Nmeans,cuttoff):
    pass

import random
def initialize(dataset,key1,Nmeans):
    Nneighbors=1200/(2*Nmeans)
    new_dataset=dataset
    initial_set=[key1]
    updated_keys=set(new_dataset.keys())
    for i in range(Nmeans-1):
        kneighbors=getNeighbors(new_dataset,new_dataset[key1],Nneighbors)
        updated_keys=updated_keys-set(kneighbors)
        key1=random.sample(updated_keys,1)
        initial_set.append(key1)
    return(initial_set)


def KM_plus_plus(dataset, Nmeans, cuttoff):
    initial=random.sample(dataset.keys(),1)
    initial_clusters=initialize(dataset,initial[0],Nmeans)
    KMeans(dataset,initial_clusters,Nmeans,cuttoff)