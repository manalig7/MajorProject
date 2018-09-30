"""
Minimal Feature Set: 
Number of unique words
Complexity
Gunning-Fog-
Character count with whitespace-
Character count without whitespace
Average syllables per word-
Sentence count-
Average sentence length-
Flesch Kincaid-
"""
import pandas as pd  
import numpy as np
import sys
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize

tsv = 'FakeNewsNet_Dataset/fakenewsnet_train.txt'
f=open(tsv,'r')
x_train=[]
y_train=[]

for line in f:
	ls=line.split('\t')
	x_train.append(ls[0].lower())
	y_train.append(int(ls[1]))

feature_set=[]

for i in range(0,len(x_train)):
	feature_set.append([])

#x_train contains the list of pieces of news texts
#1st feature- Quantity (number of syllables, number of words, number of sentences)

import spacy 
from textstat.textstat import easy_word_set, legacy_round 
from textstat.textstat import textstatistics
  
 ##########################################FUNCTIONS################################# 
def break_sentences(text): 
    nlp = spacy.load('en') 
    doc = nlp(text) 
    return doc.sents 
  
# Returns Number of Words in the text 
def word_count(text): 
    sentences = break_sentences(text) 
    words = 0
    for sentence in sentences: 
        words += len([token for token in sentence]) 
    return words 
  
# Returns the number of sentences in the text 
def sentence_count(text): 
    sentences = break_sentences(text) 
    return len(sentences) 

def num_syllables(word): 
    return textstatistics().syllable_count(word) 

# Returns the average number of syllables per 
# word in the text 
def avg_syllables_per_word(text): 
    syllable = num_syllables(text) 
    words = word_count(text) 
    ASPW = float(syllable) / float(words) 
    return legacy_round(ASPW, 1) 

#Average sentence length
def avg_sentence_length(text,words,sentences): 
    #words = word_count(text) 
    #sentences = sentence_count(text) 
    average_sentence_length = float(words / sentences) 
    return average_sentence_length 

#Returns Flesch Kincaid Score
def flesch_kincaid(text,avg_sen_len,avg_syl): 
    flesch = 206.835 - float(1.015 * avg_sen_len) -\ 
          float(84.6 * avg_syl) 
    return legacy_round(flesch, 2) 

   # Return total Difficult Words in a text 
def difficult_words(text): 
  	# Find all words in the text 
    words = [] 
    sentences = break_sentences(text) 
    for sentence in sentences: 
        words += [token for token in sentence] 
    diff_words_set = set() 
    for word in words: 
        syllable_count = syllables_count(word) 
        if word not in easy_word_set and syllable_count >= 2: 
            diff_words_set.add(word) 

def gunning_fog(text,wordcount,avg_sen_len): 
    per_diff_words = (difficult_words(text) / wordcount * 100) + 5
    grade = 0.4 * (avg_sen_len + per_diff_words) 
    return grade 
  

##############################################FEATURES################################
#Features are being stored in feature set

#Number of Words 

for i in range(0,len(x_train)):
	text=x_train[i]
	wordcount=word_count(text)
	

#Number of Sentences (0)
for i in range(0,len(x_train)):
	text=x_train[i]
	sentencecount=sentence_count(text)
	feature_set[i].append(sentencecount)

#Average Number of Syllables per word (1)
for i in range(0,len(x_train)):
	text=x_train[i]
	avg_syl=avg_syllables_per_word(text)
	feature_set[i].append(avg_syl)

#Average Number of Words per sentence(2)
for i in range(0,len(x_train)):
	text=x_train[i]
	avg_sen_len=avg_sentence_length(text,wordcount,sentencecount)
	feature_set[i].append(avg_sen_len)

#Flesch Kincaid Score (3)
for i in range(0,len(x_train)):
	text=x_train[i]
	flesch=flesch_kincaid(text,avg_sen_len,avg_syl)
	feature_set[i].append(flesch)

#Gunning-Fog (4)
for i in range(0,len(x_train)):
	text=x_train[i]
	gf=gunning_fog(text,wordcount,avg_sen_len)
	feature_set[i].append(gf)

#Number of characters with whitespace (5)
for i in range(0,len(x_train)):
	text=x_train[i]
	num_char_w=len(text)
	feature_set[i].append(num_char_w)

#Number of characters without whitespace (6)
for i in range(0,len(x_train)):
	text=x_train[i]
	num_char=0
	for j in range(0,len(text)):
		if text[j]!=' ':
			num_char=num_char+1
	feature_set[i].append(num_char)

#######################################################################################