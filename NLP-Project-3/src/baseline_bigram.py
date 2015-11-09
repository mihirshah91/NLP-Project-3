'''
@author: Name         --  Net ids
         Mihir Shah   --  mgs275
         Hardik Patel --  hvp4
'''

import nltk
import re
import operator
import random



Bigrams= {}
prev_word=""
bigram=""


''' Opening training file to build the language model '''


trainFile= open("/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/train.txt")


''' Following loop builds the unigram dictionary where key is the unigram and value is another dictionary
    which will store the labels and its count. unigram with label 'O' will be skipped 
 '''


count=0;

for line in trainFile:
    line=line.rstrip("\r\n")
    count+=1
    if(count == 1):
        sentence= line.split()
    if(count == 3):
        seq_tag= line.split()
        prev_word=" "
        current_index=0
                
        for word in sentence:
            bigram = prev_word + " " + word
           
            tag= seq_tag[current_index]
            if (tag != 'O'):
                tag=tag.split('-')
                if bigram in Bigrams: 
                    temp_dict= Bigrams[bigram]
                    if tag[1] in temp_dict:
                        temp_dict[tag[1]]+=1
                        
                    else:
                        temp_dict[tag[1]]=1
                    Bigrams[bigram]=temp_dict    
                else: 
                    temp_dict={}
                    temp_dict[tag[1]]=1
                    Bigrams[bigram] = temp_dict
            
            prev_word = word
            current_index+=1
        count=0    


''' opening the test file for predicting the tags '''

testFile= open("/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/test.txt")

'''
Following loop does the work of sequence tagging. It will take one unigram from test and will find it in train
If found in train, then assign it that label which has the max count in train. If not found in train then ignore it

'''

count=0;
results={"PER": "","LOC": "","ORG": "","MISC": "" }

for line in testFile:
    line=line.rstrip("\r\n")
    count+=1
    if(count == 1):
        sentence= line.split()
    if(count == 3):
        positions= line.split()
        prev_word=" "
        prev_entity = ""
        current_index=0
        start_index=-1
        last_index=-1
        current_entity=""
               
        for word in sentence:
            bigram = prev_word + " " + word
    
      
            
            if bigram in Bigrams: 
                temp_dict= Bigrams[bigram]
                key = max(temp_dict, key=temp_dict.get)
                current_entity=key
                
                if (start_index != -1):
                    if (current_entity == prev_entity):
                        last_index=positions[current_index]
                        
                    else:
                        temp_string=start_index + "-" + last_index
                        temp1= results[prev_entity]
                        temp1= temp1 + " " + temp_string
                        results[prev_entity]=temp1
                        
                        start_index = positions[current_index]
                        last_index = start_index 
                            
                            
                else:
                    start_index=positions[current_index]
                    last_index=start_index
                
                
                prev_entity=current_entity
                    
            else:
                
                temp_string = ""
                if (start_index != -1):
                    temp_string= start_index + "-" + last_index
                    temp1= results[current_entity]
                    temp1= temp1 + " " + temp_string
                    results[current_entity]=temp1 
                
                start_index=-1;
                last_index=-1;    
                                   
            prev_word = word
            
            current_index+=1
        count=0    


print('LOC')
print(results['LOC'])
print('PER')
print(results['PER'])
print('ORG')
print(results['ORG'])
print('MISC')
print(results['MISC'])





















