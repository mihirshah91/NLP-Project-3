'''
@author: Name         --  Net ids
         Mihir Shah   --  mgs275
         Hardik Patel --  hvp4
'''

import nltk
import re
import operator
import random


words= []
sentence= []
Bigrams= {}
vocabulary={}
prev_word=""
lines1=[]
bigram=""
delimitor_dictionary={}
delimitor_count=0
random_sentence=""
seeding_bigram=""
test=[1,2,3]
history_bigrams_probability={}



trainFile= open("/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/train.txt")




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
        #print(sentence)
        #print(len(sentence))
        #print(seq_tag)
        #print(len(seq_tag)) 
        if(len(seq_tag) != len(sentence)):
            print(sentence)
            print(seq_tag)  
        for word in sentence:
            bigram = prev_word + " " + word
            
            #print(current_index)
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



print(Bigrams)

testFile= open("/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/test.txt")


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
        #print(sentence)
        #print(len(sentence))
        #print(seq_tag)
        #print(len(seq_tag)) 
       
        for word in sentence:
            bigram = prev_word + " " + word
            
            #print(current_index)
            
            
            if bigram in Bigrams: 
                temp_dict= Bigrams[bigram]
                key = max(temp_dict, key=temp_dict.get)
                #keys = [k for k,v in temp_dict.items() if v==maxval]
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





















