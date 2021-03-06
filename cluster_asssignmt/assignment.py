from nltk.corpus import stopwords
from nltk import PorterStemmer
from collections import Counter
import math
import operator
import random

#import re
stemmer=PorterStemmer()
stopwordList=stopwords.words("english")
stopwordList2=["Hi","tell","Mr","feel","To","A","go","goes","He","he",
"she","She","They","they","The","His","Not",'',"But","come","move","away",
"Through","ask","asks","isn't",'1','2','3','4','5','6','7','8','9','0',"things",
"things","find","finds","after","before","get","got","whose","whom","Having","taken","tells"]
punctuation = '.,:;!?{}-_"'
N=1200
def sanitize(doc):
    for value in punctuation:
        doc = doc.replace(value, '')
    doc_list=[word for word in doc.split(' ') if word not in stopwordList]
    doc_list=list(set(doc_list)-set(stopwordList2))
    return(doc_list)

def count_terms(head,tokens,tf_idf_dict,idf):
    cnt=Counter(tokens)        #counts the no.of times a word appeared in the text, returns a counter obj.
    tf_idf_dict[head]=dict(cnt)  #cunverts the counter obj. into dictionary
    for key in list(cnt.keys()):   #to keep a track of no. of documents in which a word apeared
        if key in idf.keys():
            idf[key]=idf[key]+1
        else:
            idf[key]=1
    return(tf_idf_dict,idf)
'''
our definition of tf-idf:
tf_idf=(d/D)*log(N/n)
d=no. of times a term 'X' appears in a document
D= totalno. of terms in the document
N=total no. of documents
n=total no. of docuemnts in which that particular term 'X' appears
'''
def compute_tf_idf(tf_idf_dict,idf):  #computes the tf-idf as per the formula given above in comments
    N=float(len(tf_idf_dict))    
    for key in tf_idf_dict.keys():
        sum_t=float(sum(tf_idf_dict[key].values()))
        tf_idf_dict[key].update((x,((y/sum_t)*math.log(N/idf[x]))) for x,y in tf_idf_dict[key].items())
    return(tf_idf_dict)

def euclidean(vector1,vector2):  #computes euclidean distance between 2 vectors
    distance = 0
    key_set=set(vector1.keys()).union(set((vector2.keys())))
    for x in key_set:
        distance += pow((vector1.get(x,0) - vector2.get(x,0)), 2)
    return math.sqrt(distance)
 
def getNeighbors(dataset, vector, k):  #returns the id of nearest neighbors
    distances = []                     # searches the nearest k neighbors
    for x in dataset.keys():          # on the basis of euclidean distance between them
        dist = euclidean(vector, dataset[x])
        distances.append([x, dist])
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def knn(dataset,vector,idf):  #k-nearest neighbor search 
    N=len(dataset)
    vector=sanitize(vector)  # works with the given input string e.g. "hello world. This is python"
    vector=dict(Counter(vector))
    sum_t=sum(vector.values())
    vector.update((x,(y/sum_t)*math.log(N/idf[x])) for x,y in vector.items())
    neighbors=getNeighbors(dataset,vector,2)
    print(neighbors)

def initialize_KM_plus(dataset,key1,Nmeans):  #initializes first set of centroids for k-means++
    Nneighbors=N/(2*Nmeans)
    new_dataset=dataset
    initial_set=[key1]
    updated_keys=set(new_dataset.keys())
    for i in range(Nmeans-1):
        kneighbors=getNeighbors(new_dataset,new_dataset[key1],Nneighbors)
        updated_keys=updated_keys-set(kneighbors)
        key1=random.sample(updated_keys,1)
        initial_set.append(key1)
    return(initial_set)

def KM_plus_plus(dataset, Nmeans, cuttoff):  #K-means plus plus calling function
    initial=random.sample(dataset.keys(),1)
    initial_clusters=initialize_KM_plus(dataset,initial[0],Nmeans)
    KMeans(dataset,initial_clusters,Nmeans,cuttoff)

def call_kmeans(dataset,Nmeans,cutoff):  # simple k-means calling function
    initial_clusters=random.sample(dataset.keys(),Nmeans)
    KMeans(dataset,initial_clusters,Nmeans,cutoff)
    
def recompute_centroids(dataset,clusters):  # function to recompute centroids for k-means
    new_centroids=[{} for i in range(len(clusters))]
    for i in range(len(clusters)):
        for key in clusters[i]:
            for x in dataset[key].keys():
                new_centroids[i][x]=new_centroids[i].get(x,0)+dataset[key][x]
    return(new_centroids)   

def KMeans(dataset,centroids,Nmeans,cutoff):  #simple k-means
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
        if check_cutoff<cutoff:    # if difference b/w previous and new set of centroids is less
            return(new_centroids)  # than cutoff then break the loop

#def main():
filepath="P:\PGDBA\ISI\CDS\Assignment2_clustering\plot_summaries_1200.txt"
lines=open(filepath,encoding="utf8")
count=0
tf_idf_dict={}
idf={}
for line in lines:
    pos=0
    for c in line:
        if c in '0123456789':
            pos=pos+1
        else:
            break
    head=line[:pos]
    tail=line[pos:].strip()
    tokens=sanitize(tail)
    tf_idf_dict,idf=count_terms(head,tokens,tf_idf_dict,idf)
    if count==3:
        break
    count=count+1
tf_idf_dict=compute_tf_idf(tf_idf_dict,idf)
    
    
    

