# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 17:27:58 2022

@author: Team Lego Coders
"""
import datetime
import os
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
######################FILE HANDLING###########################################

def generate_mom(transcript_file):   
    def remove_blank(file1, file2):
        with open(file1) as infile, open(file2, 'w') as outfile:
            for line in infile:
                if not line.strip(): continue  # skip the empty line
                outfile.write(line)
        #     infile.close()
    print("inside generate_mom")
    remove_blank(transcript_file, 'output.txt')
    file = open("output.txt", 'r', encoding='utf-8')
    filedata = file.readlines()
    participant_list = []
    questions_asked = []
    timestamp = ""
    lineNo = 0
    discussion = []
    prevName = ""
    for line in filedata:
        if line.strip():
            if lineNo == 0:
                
                lineNo = 9999
                saveInd = line.index(']')
                timestamp = line[saveInd+1:saveInd+10]    
            if line[0] == '[':
                my_ind = line.index(']')
                name = line[1:my_ind]
                if name not in participant_list:
                    participant_list.append(name)
            prevName = name
            x = len(line)
            if line[0] == '[':
                continue
            else:
                if line[x-2] == '?':
                    questions_asked.append(prevName + ": " + line)
                else:
                        discussion.append(prevName + ": " + line)
    current_day = datetime.datetime.today()
    file.close()
    with open('temp_q.txt', 'w') as qp:
        for line in questions_asked:
            
            qp.write(line); qp.write('\n')

    qp.close()   

    with open('temp_d.txt', 'w') as d:
        for line in discussion:
            if line.strip():
                d.write(line); d.write('\n')
    d.close()
    remove_blank('temp_d.txt', 'temp_d_1.txt')
    remove_blank('temp_q.txt', 'temp_q_1.txt')
    parName = ", ".join([str(item) for item in participant_list])
    ##############################################################################
    #below dependency are for nltk work


    def read_article(file_name):
    
        file = open(file_name, 'r')
        filedata = file.readlines()
    
        article = filedata
    
        sentences = []
        for sentence in article:
        
            sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        sentences.pop()
    
        return sentences


    def sentence_similarity(sent1, sent2, stopwords=None):
    
        if stopwords is None:
            stopwrds = []
        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]
        all_words = list(set(sent1 + sent2))
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)
        
        for w in sent1:
        
            if w in stopwords:
                continue
            vector1[all_words.index(w)]  += 1
    
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)]  += 1
        return 1 - cosine_distance(vector1, vector2)    
            

    def get_sim_matrix(sentences, stop_words):
    
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
        for idx1 in range(len(sentences)): 
            for idx2 in range(len(sentences)):
                if idx1 == idx2:
                    continue
                similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
        return similarity_matrix

    def generat_summary(file_name, top_n=5):
        stop_words = stopwords.words('english')
        summarize_text = []
        sentences = read_article(file_name)
        
        sentence_similarity_matrix = get_sim_matrix(sentences, stop_words)
    
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    
        scores = nx.pagerank(sentence_similarity_graph)
        
        ranked_sentence = sorted(((scores[i], s)for i,s in enumerate(sentences)))
        
        for i in range(top_n):
        
            summarize_text.append(" ".join(ranked_sentence[i][1]))
            
        return summarize_text

    number = 1  
    with open('your_mom.txt', 'w') as op:
        
        op.write('MOM From Call on ' + str(current_day)[:10] + " at" + timestamp); op.write('\n')
        op.write('-' * 40); op.write('\n')
        op.write('\n')
        op.write("Participants :" + parName);
        op.write('\n');op.write('-' * len("Participants :" + parName)); op.write('\n')
        op.write('\n')
        final = generat_summary('temp_d_1.txt', 10)
        op.write("Discussion :") ; op.write('\n')
        op.write('*' * 12); op.write('\n')
        for line in final:
            
            line = str(number) + ". " + line
            op.write(line); 
            number +=1
        
        ques = open('temp_q_1.txt', 'r', encoding='utf-8')
        op.write('\n')
        ques_data = ques.readlines()
        op.write("Questions Raised :");op.write('\n')
        op.write('*' * 18); op.write('\n')
        for q in ques_data:
            op.write(q)
        op.close()    
        ques.close()        

    os.remove('output.txt')  
    os.remove('temp_d.txt')  
    os.remove('temp_d_1.txt')   
    os.remove('temp_q.txt') 
    os.remove('temp_q_1.txt') 
    return 'your_mom.txt'       
            
        
            
        



    