

# Importing the required Libraries
import numpy as np
import pandas as pd
import nltk
#nltk.download('punkt') # one time execution
import re
#nltk.download('stopwords') # one time execution


from nltk.tokenize import sent_tokenize

from nltk.corpus import stopwords

from sklearn.metrics.pairwise import cosine_similarity

import networkx as nx

word_embeddings = {}
file = open('glove.6B.100d.txt', encoding='utf-8')
for line in file:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
file.close()
len(word_embeddings)

# function to remove stopwords
def remove_stopwords(sen):
    stop_words = stopwords.words('english')
    
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

# function to make vectors out of the sentences
def sentence_vector_func (sentences_cleaned) : 
    sentence_vector_gen = []
    for i in sentences_cleaned:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vector_gen.append(v)
    
    return (sentence_vector_gen)

#Function to return summary
    
def summary_text (test_text, n = 5):
    sentences = []
    
    # Here we are tokenising the text 
    sentences.append(sent_tokenize(test_text))
    sentences = [y for x in sentences for y in x] # flatten list
    
    # remove punctuations, numbers and special characters
    clean_sentences = pd.Series(sentences).str.replace("[^a-z A-Z 0-9]", " ")

    # make alphabets in lowercase
    clean_sentences = [s.lower() for s in clean_sentences]
    
    # remove stopwords from the sentences
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
    #print(clean_sentences)
    
    sentence_vectors = sentence_vector_func(clean_sentences)
    
    # creating similarity matrix of sentences
    similarity_matrix = np.zeros([len(sentences), len(sentences)])
    
    # Finding the similarities between the sentences 
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
    
    
    nex_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nex_graph)
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)))
    
    # Extract and return sentences as the summary
    summarised_text_string = ''
    for i in range(n):
        
        try:
            summarised_text_string = summarised_text_string + str(ranked_sentences[i][1])            
        except IndexError:
            print ("Summary Not generated")
    
    return (summarised_text_string)


