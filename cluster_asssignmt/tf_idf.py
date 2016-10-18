# -*- coding: utf-8 -*-
'''
our definition of tf-idf:
d=no. of times a term appears in a document
D= totalno. of terms in the document
N=total no. of documents
n=total no. of docuemnts in which that particular word appears

tf_idf=(d/D)*log(N/n)

'''
N=1200
from nltk.corpus import stopwords
from nltk import PorterStemmer
from collections import Counter
from math import log
stemmer=PorterStemmer()
stopwordList=stopwords.words("english")
stopwordList2=["Hi","To","A","go","goes","He","he","she","She","They","they","The","His","Not",'',"But","come","move","away","Through","ask","asks","isn't",'1','2','3','4','5','6','7','8','9','0',"things","things","find","finds","after","before","get","got","whose","whom","Having","taken","tells"]
punctuation = '.,:;!?{}-_"'

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
    
def compute_tf_idf(tf_idf_dict,idf):  #computes the tf-idf as per the formula given at the top in comments
    for key in tf_idf_dict.keys():
        sum_t=sum(tf_idf_dict[key].values())
        tf_idf_dict[key].update((x,((y/sum_t)*log(N/idf[x]))) for x,y in tf_idf_dict[key].items())
            
        
        
