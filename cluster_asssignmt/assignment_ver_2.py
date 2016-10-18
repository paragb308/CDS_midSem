from nltk.corpus import stopwords
from nltk import PorterStemmer
from collections import Counter
import math
import operator
import random
import csv
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
    Nneighbors=30
    new_dataset=dataset
    initial_set=[key1]
    #print("initial_set",initial_set)
    updated_keys=set(new_dataset.keys())
    #print("updated_keys:",updated_keys)
    for i in range(Nmeans-1):
        #print("OK")
        kneighbors=getNeighbors(new_dataset,new_dataset[initial_set[i]],Nneighbors)
        #print(kneighbors)
        updated_keys=updated_keys-set(kneighbors)
        #print("updated_keys:",updated_keys)
        key1=random.sample(updated_keys,1)
        #print("key1",str(key1[0]))
        initial_set.append(str(key1[0]))
        #print("initial_set_itr 2",initial_set)
    return(initial_set)
    
def recompute_centroids(dataset,clusters):  # function to recompute centroids for k-means
    new_centroids=[{} for i in range(len(clusters))]
    for i in range(len(clusters)):
        for key in clusters[i].keys():
            for x in dataset[key].keys():
                new_centroids[i][x]=new_centroids[i].get(x,0)+dataset[key][x]
        div=len(clusters[i].keys())
        for key in new_centroids[i].keys():
            new_centroids[i][key]=new_centroids[i][key]/div         
    return(new_centroids)   

def KMeans(dataset,centroids,Nmeans,cutoff):  #simple k-means 
   # print(clusters)
    while(True):
        clusters = [{} for c in centroids]
        for key in dataset.keys():
           # print(dataset[key])
            #print(dataset[centroids[0]])
            smallest_distance = euclidean(dataset[key], centroids[0])
            clusterIndex = 0
            for i in range(1,len(centroids)):
                distance = euclidean(dataset[key], centroids[i])
                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex =i
            clusters[clusterIndex][key]=smallest_distance
        new_centroids=recompute_centroids(dataset,clusters) #recompute new centroids for clusters
        check_cutoff=0
        for i in range(Nmeans):
            check_cutoff+=euclidean(centroids[i],new_centroids[i])
        check_cutoff=check_cutoff/Nmeans
        centroids=new_centroids
        if check_cutoff<cutoff:    # if difference b/w previous and new set of centroids is less
            return(clusters)  # than cutoff then break the loop

def call_kmeans(dataset,Nmeans,cutoff):  # simple k-means calling function
    initial_centroids_keys=random.sample(dataset.keys(),Nmeans)
    initial_centroids=[{} for x in range(Nmeans)]
    for i in range(Nmeans):
        initial_centroids[i]=dataset[initial_centroids_keys[i]]
    clusters=KMeans(dataset,initial_centroids,Nmeans,cutoff)
    return(clusters)
    #return(initial_centroids)
    
def KM_plus_plus(dataset, Nmeans, cuttoff):  #K-means plus plus calling function
    initial=random.sample(dataset.keys(),1)
    initial_centroids_keys=initialize_KM_plus(dataset,initial[0],Nmeans)
    initial_centroids=[{} for x in range(Nmeans)]
    for i in range(Nmeans):
        initial_centroids[i]=dataset[initial_centroids_keys[i]]
    clusters=KMeans(dataset,initial_centroids,Nmeans,cuttoff)
    return(clusters)

def name_tags (clusters,meta_data):
    named_clusters=[[] for x in range(len(clusters))]
    reader = csv.reader(open(meta_data,encoding="ISO-8859-1"))
    meta_data = {}
    for row in reader:
        k, v = row
        meta_data[k] = v
    for i in range(len(clusters)):
        for key in clusters[i].keys():
            named_clusters[i].append(meta_data[key])  
    return(named_clusters)  
            
def main():
    filepath="S:/Assignments/CDS/plot_summaries_1200.txt"
    meta_data="S:/Assignments/CDS/meta_data_1200.csv"
    lines=open(filepath,encoding="ISO-8859-1")
    #count=0
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
        #if count==100:
         #   break
        #count=count+1
    tf_idf_dict=compute_tf_idf(tf_idf_dict,idf)
    #print(tf_idf_dict)
    #clusters=call_kmeans(tf_idf_dict,150,0.5)
    clusters=KM_plus_plus(tf_idf_dict,50,0.5)
    named_clusters=name_tags(clusters,meta_data)
    for i in range(len(named_clusters)):
        print()
        print("cluster:",named_clusters[i])
        print()
        print()
    
if __name__=="__main__":
    main()
    

