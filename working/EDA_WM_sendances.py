# Geoff's hacking to explore data.
# Some time conversion and extraction of sentence count may be useful later
# coding: utf-8
import nltk
from nltk.tokenize import sent_tokenize

import pymongo
import pandas as pd
import numpy as np

from pymongo import MongoClient
from bson.objectid import ObjectId

import datetime

from collections import Counter

import matplotlib.pyplot as plt

from collections import defaultdict


# get_ipython().magic(u'matplotlib inline')
import json
plt.style.use('ggplot')


# In[2]:

## Connect to local DB

client = MongoClient('localhost', 27017)
print("Setup db access")


# In[4]:

#
# Get collections from mongodb
#
db = client.wootmath
reponses = db.anon_student_task_responses.find()


# In[6]:

df_responses = pd.DataFrame(list(reponses))


# In[7]:

print(df_responses.head())


# In[9]:

print(df_responses.columns)


# In[10]:

print(len(df_responses), "Number of entries")


# In[13]:

print("Unique lessions", df_responses['lesson'].unique())

time_spent = df_responses['time_spent']
correct = df_responses['correct']
timestamps = df_responses['timestamp']
times = [datetime.datetime.fromtimestamp(timestamp/1000.0) for timestamp in timestamps]
minutes = [ (time.hour * 60 + time.minute) for time in times]
bonus = df_responses['bonus']
level_summaries = df_responses['level_summary']

subjects = [level_summaries[x]['subject'] for x in range(0, len(level_summaries))]
countCorrect = Counter(correct)
txt = df_responses['txt']

sentence_lengths = [len(sent_tokenize(instructions)) for instructions in txt]

# print("time of days:", times)
# print("minutes:", minutes)
pairs = list(zip(sentence_lengths, correct))
numSentencesCorrect = [entry[0] for entry in pairs if entry[1] == True]
numSentences = [entry[0] for entry in pairs ]
countCorrect = Counter(numSentencesCorrect)
countTotal = Counter(numSentences)
ratioCorrect = [countCorrect[key] / countTotal[key] for key in countTotal]
ratioDict = dict(zip(countTotal, ratioCorrect))
globalCorrectRatio = Counter(correct)[True] / len(df_responses)
sentences_and_lengths = list(zip(txt,sentence_lengths))
bad_sentences_and_lengths = [x for x in sentences_and_lengths if x[1] == 7]
print("Examples with 7 sentences")
for sentence, count in bad_sentences_and_lengths:
    sentence = str.replace(sentence, "\n","")
    print(sentence)

plt.bar(list(ratioDict.keys())[0:4], list(ratioDict.values())[0:4])
plt.axhline(y=globalCorrectRatio, color='b', linestyle='-', label="Global Correct \%")
# plt.show()
plt.title("sentence length effect on correct response")
plt.xlabel("sentences in pb description")
plt.ylabel("ratio correct")
plt.savefig("sentence_length_correct.png")


print("correct:", len([c for c in correct if c == True]))
print("incorrect:", len([c for c in correct if c == False]))
# In[ ]:



