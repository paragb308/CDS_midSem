import math
import operator
from nltk.corpus import stopwords
from nltk import PorterStemmer
from collections import Counter


stemmer=PorterStemmer()
stopwordList=stopwords.words("english")
stopwordList2=["Hi","tell","Mr","feel","To","A","go","goes","He","he","she","She","They","they","The","His","Not",'',"But","come","move","away","Through","ask","asks","isn't",'1','2','3','4','5','6','7','8','9','0',"things","things","find","finds","after","before","get","got","whose","whom","Having","taken","tells"]
punctuation = '.,:;!?{}-_"'

def sanitize(doc):
    for value in punctuation:
        doc = doc.replace(value, '')
    doc_list=[word for word in doc.split(' ') if word not in stopwordList]
    doc_list=list(set(doc_list)-set(stopwordList2))
    return(doc_list)

def euclidean(vector1,vector2):
    distance = 0
    key_set=set(vector1.keys()).union(set((vector2.keys())))
    for x in key_set:
        distance += pow((vector1.get(x,0) - vector2.get(x,0)), 2)
    return math.sqrt(distance)

def compute_tf_idf(tf_idf_dict,idf):  #computes the tf-idf as per the formula given above in comments
    N=float(len(tf_idf_dict))    
    for key in tf_idf_dict.keys():
        sum_t=float(sum(tf_idf_dict[key].values()))
        tf_idf_dict[key].update((x,((y/sum_t)*math.log(N/idf[x]))) for x,y in tf_idf_dict[key].items())
    return(tf_idf_dict)
    
def getNeighbors(dataset, vector, k):  #returns the id of nearest neighbors
	distances = []
	for x in dataset.keys():
		dist = euclidean(vector, dataset[x])
		distances.append([x, dist])
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def knn(dataset,vector,idf):
    N=len(dataset)
    vector=sanitize(vector)
    vector=dict(Counter(vector))
    sum_t=sum(vector.values())
    vector.update((x,(y/sum_t)*math.log(N/idf[x])) for x,y in vector.items())
    neighbors=getNeighbors(dataset,vector,2)
    print(neighbors)
''' ---------------------------------TESTING -----------------------------------------------
def main():
    dataset={'10001':{'else': 2, 'conversation': 2, 'unclefree': 2, 'room': 2},
    '10002':{'else': 4, 'thought': 4, 'concerned': 4, 'uncomfortable': 4},
    '10003':{'conversation': 1, 'unclefree': 1, 'room': 1}}
    vector="this is conversation unclefree room so do you need it?"
    knn(dataset,vector)
if __name__=="__main__":
    main()
'''