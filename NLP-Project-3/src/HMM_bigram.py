'''
@author: Name         --  Net ids
         Mihir Shah   --  mgs275
         Hardik Patel --  hvp4
'''

import nltk
import re
import operator
import random
import collections


Unigrams= {}
tagCounts={"O":0,"B-PER":0,"I-PER":0,"B-ORG":0,"I-ORG":0,"B-LOC":0,"I-LOC":0,"B-MISC":0,"I-MISC":0}
tagBigrams={}
tagBigramsProbability={}
unknown=[]
#global global_counternew
global_counternew=0

Unigrams['unknown']={}
vocabulary={}
totalWords=0.0
numberOfTags=9
startProb={"O":0,"B-PER":0,"I-PER":0,"B-ORG":0,"I-ORG":0,"B-LOC":0,"I-LOC":0,"B-MISC":0,"I-MISC":0}
tags={"O","B-PER","I-PER","B-ORG","I-ORG","B-LOC","I-LOC","B-MISC","I-MISC"}


'''test1234'''
''' Opening training file to build the language model '''

trainFile= open("/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/data_sets/training_set_2")
#trainFile= open("/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/train.txt")

def make_probability_table(prev_word,word):

    if prev_word in tagBigramsProbability:
        temp_dict=tagBigramsProbability[prev_word]
        if word in temp_dict:
         temp_dict[word]+=1
        else : temp_dict[word]=1    
        tagBigramsProbability[prev_word]=temp_dict 
    else:
        temp_dict={"O":0,"B-PER":0,"I-PER":0,"B-ORG":0,"I-ORG":0,"B-LOC":0,"I-LOC":0,"B-MISC":0,"I-MISC":0}
        temp_dict[word]=1
        #temp_dict={word:1}
        tagBigramsProbability[prev_word]=temp_dict



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
               
        startProb[seq_tag[0]]+=1
                  
        for word in sentence:            
            
            tag= seq_tag[current_index]
            bigram= prev_tag+" "+tag
            totalWords+=1            

            if word in vocabulary:
                vocabulary[word]+=1
            else:
                vocabulary[word]=1

            if bigram in tagBigrams:
                make_probability_table(prev_tag,tag)
                tagBigrams[bigram]+=1
            else:
                make_probability_table(prev_tag,tag)
                tagBigrams[bigram]=1
            prev_tag=tag    
            
            if tag in tagCounts:
                tagCounts[tag]+=1
            else:
                tagCounts[tag]=1
            
                      
            if word in Unigrams: 
                temp_dict= Unigrams[word]
                if tag in temp_dict:
                    temp_dict[tag]+=1
                    
                else:
                    temp_dict[tag]=1
                Unigrams[word]=temp_dict    
            else: 
                if word in unknown:
                    temp_dict={"O":0,"B-PER":0,"I-PER":0,"B-ORG":0,"I-ORG":0,"B-LOC":0,"I-LOC":0,"B-MISC":0,"I-MISC":0}
                    temp_dict[tag]=1
                    Unigrams[word] = temp_dict
                else:
                    temp_dict=Unigrams['unknown']
                    if tag in temp_dict:
                        temp_dict[tag]+=1
                    else:
                        temp_dict[tag]=1
                    unknown.append(word)
                    Unigrams['unknown']=temp_dict
            
            
            current_index+=1
        tag='STOP'
        bigram=prev_tag+" "+tag
        if bigram in tagBigrams:
            tagBigrams[bigram]+=1
        else:
            tagBigrams[bigram]=1    
        count=0    

c0=totalWords/(totalWords+len(vocabulary))
print("totalwords=")
print(totalWords)
print(len(vocabulary))

f = open('/home/mihir/nlpoutput/Unigrams_unsmoothed','w')
f.write(str(Unigrams))
f.close()

f = open('/home/mihir/nlpoutput/start_prob_unsmoothed','w')
f.write(str(startProb))
f.close()


''' Add one smoothing'''

for word in Unigrams:
    temp_dict=Unigrams[word]
    temp_dict.update((x, (y+1)*c0) for x, y in temp_dict.items())
    Unigrams[word]=temp_dict

c0tags=totalWords/(totalWords+numberOfTags)

#print(c0tags)

for word in tagBigramsProbability:
    temp_dict=tagBigramsProbability[word]
    temp_dict.update((x, (y+1)*c0tags) for x, y in temp_dict.items())
    tagBigramsProbability[word]=temp_dict




#print(len(vocabulary))
#print(c0)
#print(totalWords)

''' opening the test file for predicting the tags '''

testFile= open("/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/data_sets/validation_set_2")
#testFile= open("/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/test.txt")

f = open('/home/mihir/nlpoutput/Unigrams','w')
f.write(str(Unigrams))
f.close()

f = open('/home/mihir/nlpoutput/vocabulary','w')
f.write(str(vocabulary))
f.close()

f = open('/home/mihir/nlpoutput/tagCounts','w')
f.write(str(tagCounts))
f.close()

f = open('/home/mihir/nlpoutput/tagBigrams','w')
f.write(str(tagBigrams))
f.close()

f = open('/home/mihir/nlpoutput/tagBigramsProbability','w')
f.write(str(tagBigramsProbability))
f.close()



#print(tagCounts)
#print(tagBigrams)
count=0;
results={"PER": "","LOC": "","ORG": "","MISC": "" }


'''Viterbi Algorithm'''

lambda1=0.5
lambda2=0.5
tagCountProbability= {}

for tag in tagCounts:
    tagCountProbability[tag]= tagCounts[tag]/totalWords
    


for tag in tagBigramsProbability:
    temp_dict=tagBigramsProbability[tag]
    rowSum=0.0
    rowSum+=sum(temp_dict.values())
    temp_dict.update((x, (y/rowSum)) for x, y in temp_dict.items())
    tagBigramsProbability[tag]=temp_dict


f = open('/home/mihir/nlpoutput/tagBigramsProbability1','w')
f.write(str(tagBigramsProbability))
f.close()

def calculateTransitionProb (v,u):


    bigram=u +" "+v
    if bigram in tagBigrams:
        tempValue=(tagBigrams[bigram]+1)*c0tags
    else:
        tempValue=c0tags
    #temp_dict=tagBigrams[u]
    sum=0.0
    #print("in fun"+u)
    sum = tempValue/tagCounts[u] + tagCounts[v]/totalWords
    #sum=sum+ lambda2*tagCountProbability[v]
    #print("after")
    return sum    

def calculateEmissionProb(w,tag):
    if w in Unigrams:
        temp_dict=Unigrams[w]
    else:
        temp_dict=Unigrams['unknown']
    if tag not in temp_dict:
        temp_dict[tag]=c0
    sum=temp_dict[tag]/tagCounts[tag]
    return sum

#print(startProb)
'''cal satrt prob'''
''' Add one smoothing for start prob'''


startsum=0.0
startsum+=sum(startProb.values())
c0tags=startsum/(startsum+numberOfTags)
startProb.update((x, (y+1)*c0) for x, y in startProb.items())

#print(startsum)
startProb.update((x, (y/startsum)) for x, y in startProb.items())


'''
Following loop does the work of sequence tagging. It will take one unigram from test and will find it in train
If found in train, then assign it that label which has the max count in train. If not found in train then ignore it

'''

def viterbi(sentence):
    # initilization step:

    #print("inside")
    #print(sentence)
    global global_counternew
    
    maxProb=collections.defaultdict()
    backPointers=collections.defaultdict()
    sequence=""
    for state in tags:
        maxProb[(0,state)]= startProb[state] * calculateEmissionProb(sentence[0],state)
                     
    for k in range(1,len(sentence)):
        #print("k=")
        #print(k)
        for curr_tag in tags:

            #maxProb[(k,curr_tag)]= max(maxProb[(k-1,tag)]* calculateTransitionProb(curr_tag,tag)*calculateEmissionProb(sentence[k],curr_tag) for tag in tags)

            maxValue=0.0
            state=""
            for tag in tags:
                temp=maxProb[(k-1,tag)]* calculateTransitionProb(curr_tag,tag)*calculateEmissionProb(sentence[k],curr_tag)
                if(temp>maxValue):
                    maxValue=temp
                    state=tag
            maxProb[(k,curr_tag)]=maxValue
            backPointers[(k,curr_tag)]=state
    #print(maxProb)
            #print(backPointers)
    for k in range(len(sentence)-1,0,-1):
        maxValue=0.0
        #print("indwsfddf")
        seqtag=""
        for tag in tags:
            temp=maxProb[(k,tag)]
            if(temp>maxValue):
                maxValue=temp
                seqtag=tag
      
                
        if(k==(len(sentence)-1)):
            sequence+=seqtag        
        sequence= backPointers[(k,seqtag)]+ " "+sequence
    tempprint=""
    
    
    # print("seq="+sequence)
    # for k in range(0,len(sentence)):
    #     print global_counternew,
    #     global_counternew+=1
    # print
    #print("pos="+temp_string)
    return sequence
#def maxProbability(curr_tag,k,word):

    

count=0;
results={"PER": "","LOC": "","ORG": "","MISC": "","O":"" }


current_index=-1
start_index=0
last_index=-1
flag=0

global_counternew=0

for line in testFile:
    line=line.rstrip("\r\n")
    count+=1
    if(count == 1):
        sentence= line.split()
    if(count == 3):
        positions= line.split()
        #start_index=current_index
        #print("sentence"+str(sentence))
        
        sequence=viterbi(sentence)

        count=0
        
        if sequence:
            if(flag==1):
                start_index=current_index+1
                last_index=current_index+1
            flag=1

            tag_list=sequence.split()
            if (tag_list[0]=='O'):
                prev_tag=tag_list[0]
            else:
                prev_tag = (tag_list[0].split('-'))[1]   



            for tag in tag_list:
                current_index+=1

                if(tag!='O'):
                    curr_tag=tag.split('-')[1]
                else:
                    curr_tag='O'

                if(prev_tag==curr_tag):
                    last_index=current_index
                else:
                    temp=results[prev_tag]
                    new_string=str(start_index)+"-"+str(last_index)
                    temp=temp + " "+ new_string
                    results[prev_tag]=temp
                    start_index=current_index
                    last_index=current_index    
                prev_tag=curr_tag
            
            temp=results[curr_tag]
            new_string=str(start_index)+"-"+str(last_index)
            if(temp==""):
                temp=temp+new_string
            else:
                temp=temp + " "+ new_string
            results[curr_tag]=temp
           
        # initializtion

print('LOC')
print(results['LOC'])
print('PER')
print(results['PER'])
print('ORG')
print(results['ORG'])
print('MISC')
print(results['MISC'])

f = open('/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/results/results9.csv','w')
f.write('Type,Prediction\n')
f.write('LOC,')
f.write(results['LOC'])
f.write('\n')
f.write('PER,')
f.write(results['PER'])
f.write('\n')
f.write('ORG,')
f.write(results['ORG'])
f.write('\n')
f.write('MISC,')
f.write(results['MISC'])

f.close()

        




            
           












