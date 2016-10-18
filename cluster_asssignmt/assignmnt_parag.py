def readData(filename):
    fileobj = open(filename, encoding = "utf-8")
    film_desc = []
    film_no = []
    import re
    for line in fileobj:
        no, desc = re.split(" |\t", line, 1)
        film_desc.append(desc)
        film_no.append(no)
    fileobj.close()
    return dict(zip(film_no, film_desc))

def sanitize(text):

    from nltk.stem.snowball import SnowballStemmer
    stemmer = SnowballStemmer("english")

    import nltk as nltk
    from nltk.corpus import stopwords
    import re

    tokens = [word
              for sent in nltk.sent_tokenize(text)
              for word in nltk.word_tokenize(sent)]

    # removing punctuation and digits
    filtered_tokens = []
    for token in tokens:
        if re.search("[a-zA-Z]", token):
            filtered_tokens.append(token)

    filtered_tokens = [word for word in filtered_tokens if word not in stopwords.words('english')]

    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def count_tf_n_df(data_row_head, data_row):
    from collections import Counter
    word_occur = Counter(data_row)
    tf_dict[data_row_head] = dict(word_occur)  # Counter finds occurrence for each element in the list

    for word in word_occur.keys():
        if word in df_dict.keys():
            df_dict[word] += 1
        else:
            df_dict[word] = 1

def compute_tfidf():
    import math
    total_rows = len(tf_dict)
    for row in tf_dict.keys():
        total_words = sum(tf_dict[row].values())
        for word, count in tf_dict[row].items():
            new_weight = count / total_words * math.log(total_rows / df_dict[word])
            tf_dict[row][word] = new_weight

def getKNN(givenRowKey, NNCount):

    if len(tf_dict.keys()) <= NNCount:
        return "Number of k nearest neighbours should be less than number of all neighbours"
    import operator
    distances = {}
    for row in tf_dict.keys():
        distance = l2_distance(tf_dict[row],  tf_dict[givenRowKey])
        distances[row] = distance
    distances = sorted(distances.items(), key = operator.itemgetter(1))
    return distances[1:NNCount-1]

def l2_distance(vectorA, vectorB):
    import math
    distance = 0
    word_Set = set(vectorA.keys()).union(set(vectorB.keys()))
    for word in word_Set:
        distance += math.pow(vectorA.get(word, 0) - vectorB.get(word, 0), 2)
    return math.sqrt(distance)

def kmean(noOfClusters, cutoff_distance):
    import random
    centroids_ids = random.sample(tf_dict.keys(), noOfClusters)
    centroids = [{} for i in range(noOfClusters)]

    for i in range(noOfClusters):
        centroids[i] = tf_dict[centroids_ids[i]]

    while(True):

        clusters = [{} for i in centroids_ids]

        # Assigning points to nearest clusters
        for row_id in tf_dict.keys():
            smallest_distance = 0
            closest_cluster_index = 0

            for current_cluster in range(len(centroids_ids)):
                distance = l2_distance(tf_dict[row_id], centroids[current_cluster])
                if  current_cluster == 0 or distance < smallest_distance:
                    smallest_distance = distance
                    closest_cluster_index = current_cluster

            clusters[closest_cluster_index][row_id] = smallest_distance


        # Recomputing centroids of clusters

        new_centroids = compute_centroids(clusters)

        # Verifying cutoff criteria
        old_new_centroid_dist = 0
        for current_cluster in range(noOfClusters):
            old_new_centroid_dist += l2_distance(centroids[current_cluster], new_centroids[current_cluster])

        old_new_centroid_dist /= noOfClusters
        centroids = new_centroids

        if old_new_centroid_dist < cutoff_distance:
            return clusters

def compute_centroids(clusters):
    new_centroids = [{} for i in range(len(clusters))]

    for current_cluster in range(len(clusters)):
        for row_id in clusters[current_cluster].keys():
            for word in tf_dict[row_id].keys():
                new_centroids[current_cluster][word] = new_centroids[current_cluster].get(word, 0) \
                                                       + tf_dict[row_id][word]

        for word in new_centroids[current_cluster].keys():
            new_centroids[current_cluster][word] /= len(clusters[current_cluster].keys())

    return new_centroids

#---------------------------------Main Code-----------------------------------

#Reading Data
filename = "P:\PGDBA\ISI\CDS\Assignment2_clustering\plot_summaries_10.txt"
data = readData(filename)

# filter, tokenize and stem
tf_dict = {}
df_dict = {}

#Cleaning and Calculating TF & DF
for key in data.keys():
    # Cleaning
    data[key] = sanitize(data[key])
    # TF and DF Calculation
    count_tf_n_df(key, data[key])

# TF-IDF Weight Calculation
compute_tfidf()

# Get K NN for a row
#print(getKNN('10007089', 3))

print( kmean(5, 0.5))

