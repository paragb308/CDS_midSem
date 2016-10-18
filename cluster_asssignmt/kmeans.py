# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 01:14:56 2016

@author: DEEPANSHU
"""
import random
def euclidean(vector1,vector2):
    pass
def call_kmeans(dataset,Nmeans,cutoff):
    initial_clusters=random.sample(dataset.keys(),Nmeans)
    kMeans(dataset,initial_clusters,Nmeans,cutoff)
    
def recompute_centroids(dataset,clusters):
    new_centroids=[{} for i in range(len(clusters))]
    for i in range(len(clusters)):
        for key in clusters[i]:
            for x in dataset[key].keys():
                new_centroids[i][x]=new_centroids[i].get(x,0)+dataset[key][x]
    return(new_centroids)   

def kMeans(dataset,centroids,Nmeans,cutoff):
    clusters = [ [] for c in centroids]
    while(True):
        for key in dataset.keys():
            smallest_distance = euclidean(dataset[key], centroids[0])
            clusterIndex = 0
            for i in range(1,len(centroids)):
                distance = euclidean(dataset[key], centroids[i])
                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex =i
            clusters[clusterIndex].append(key)
        new_centroids=recompute_centroids(dataset,clusters)
        check_cutoff=0
        for i in range(Nmeans):
            check_cutoff+=euclidean(centroids[i],new_centroids[i])
        check_cutoff=check_cutoff/Nmeans
        centroids=new_centroids
        if check_cutoff<cutoff:
            return(new_centroids)
            
        
    