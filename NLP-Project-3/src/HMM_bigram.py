'''
@author: Name         --  Net ids
         Mihir Shah   --  mgs275
         Hardik Patel --  hvp4
'''

import nltk
import re
import operator
import random



Unigrams= {}
tagCounts={}
tagBigrams={}


''' Opening training file to build the language model '''

trainFile= open("/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/train.txt")


''' Following loop builds the bigram dictionary where key is the bigram and value is another dictionary
    which will store the labels and its count. Bigram with label 'O' will be skipped 
 '''

count=0;

for line in trainFile:
    line=line.rstrip("\r\n")
    count+=1
    if(count == 1):
        sentence= line.split()
    if(count == 3):
        seq_tag= line.split()
        prev_tag="*"
        current_index=0
          
          
        for word in sentence:            
            
            tag= seq_tag[current_index]
            bigram= prev_tag+" "+tag
            
            if bigram in tagBigrams:
                tagBigrams[bigram]+=1
            else:
                tagBigrams[bigram]=1
            prev_tag=tag    
            
            if tag in tagCounts:
                tagCounts[tag]+=1
            else:
                tagCounts[tag]=1
            
            if (tag != 'O'):
                tag=tag.split('-')
                if word in Unigrams: 
                    temp_dict= Unigrams[word]
                    if tag[1] in temp_dict:
                        temp_dict[tag[1]]+=1
                        
                    else:
                        temp_dict[tag[1]]=1
                    Unigrams[word]=temp_dict    
                else: 
                    temp_dict={}
                    temp_dict[tag[1]]=1
                    Unigrams[word] = temp_dict
            
            
            current_index+=1
        tag='STOP'
        bigram=prev_tag+" "+tag
        if bigram in tagBigrams:
            tagBigrams[bigram]+=1
        else:
            tagBigrams[bigram]=1    
        count=0    


''' opening the test file for predicting the tags '''

testFile= open("/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/test.txt")
print(seq_tag)
print(Unigrams)
print(tagCounts)
print(tagBigrams)
count=0;
results={"PER": "","LOC": "","ORG": "","MISC": "" }

'''
Following loop does the work of sequence tagging. It will take one bigram from test and will find it in train
If found in train, then assign it that label which has the max count in train. If not found in train then ignore it

'''

for line in testFile:
    line=line.rstrip("\r\n")
    count+=1
    if(count == 1):
        sentence= line.split()
    if(count == 3):
        positions= line.split()
        
        prev_entity = ""
        current_index=0
        start_index=-1
        last_index=-1
        current_entity=""
              
        for word in sentence:
                          
            if word in Unigrams: 
                temp_dict= Unigrams[word]
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





















