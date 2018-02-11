
# coding: utf-8

# In[1]:

import pymongo
import pandas as pd
import numpy as np

from pymongo import MongoClient
from bson.objectid import ObjectId

import datetime

import matplotlib.pyplot as plt

from collections import defaultdict


get_ipython().magic(u'matplotlib inline')
import json
plt.style.use('ggplot')

import seaborn as sns


# In[2]:

## Connect to local DB

client = MongoClient('localhost', 27017)
print ("Setup db access")


# In[3]:

#
# Get collections from mongodb
#
db = client.my_test_db
reponses = db.anon_student_task_responses.find()


# In[4]:

df_responses = pd.DataFrame(list(reponses))


# In[5]:

print (df_responses.head())


# In[6]:

## Look act columns
print (df_responses.columns)


# In[7]:

## How many data samples
print (len(df_responses), "Number of entries")


# In[8]:

## Example data samle
print (df_responses.iloc[1])


# In[9]:

print ("Number of unique lessions", len(df_responses['lesson'].unique()) )
print ("Unique lessions", df_responses['lesson'].unique())


# In[10]:

print ("Samples of each lesson",df_responses['lesson'].value_counts())


# In[11]:

print ("Summary sample :", df_responses['level_summary'][0])


# In[12]:

## Promote student info, level summary, level summary problem results


# In[13]:

df2 = df_responses.join(pd.DataFrame(df_responses["student"].to_dict()).T)


# In[14]:

df2 = df2.join(pd.DataFrame(df2['level_summary'].to_dict()).T)


# In[15]:

df2 = df2.join(pd.DataFrame(df2['problems'].to_dict()).T)


# In[16]:

df_student1 = df2.groupby('student_id').agg({ 'lesson':[len,  pd.Series.nunique ], 'ntotal':sum, 'nright':sum })


# In[17]:

df_student1['percent_correct'] = df_student1['nright']['sum'].astype(float) / df_student1['ntotal']['sum']


# In[18]:

df_student1


# In[19]:

y1 = np.array(df_student1['lesson']['len'])


# In[ ]:




# In[20]:

# Total Lessons per student

plt.title(' Number of students performing number lessons ')
plt.xlabel('Number of total lessons attempted')
plt.ylabel('Number of students')
plt.hist(y1, bins=40)




# In[21]:

# Uniqe students per # of unique lessons
y2 = np.array(df_student1['lesson']['nunique'])
plt.title(' Number of students performing lesson types')
plt.xlabel('Number of unique lessons attempted')
plt.ylabel('Number of students')
plt.hist(y2, bins=40)


# In[ ]:




# In[22]:

# Uniqe students per # of unique lessons
y3 = np.array(df_student1['percent_correct'])
plt.title(' Number of students vs problems answered correctly')
plt.xlabel('Percent of problems answered correctly')
plt.ylabel('Number of students')
plt.hist(y3, bins = 40)


# In[24]:

df2.columns


# In[25]:

df2['subject'].unique()


# In[26]:

df2.iloc[0]


# In[27]:

df2.iloc[0]['response']


# In[28]:

df_lesson1 = df2.groupby('lesson').agg({ 'student_id':[len,  pd.Series.nunique ], 'ntotal':sum, 'nright':sum })


# In[29]:

df_lesson1['percent_correct'] = df_lesson1['nright']['sum'].astype(float) / df_lesson1['ntotal']['sum']


# In[30]:

# Lessons and answers
y3 = np.array(df_lesson1['percent_correct'])
plt.title(' Lessons: percent of correct answers per lesson histogram')
plt.xlabel('Percent of problems answered correctly')
plt.ylabel('Number of lessons')
plt.hist(y3, bins = 40)


# In[34]:

df_lesson1


# In[36]:

df_lesson1.sort_values('percent_correct')


# In[ ]:




# In[37]:

df3  = df2.copy()


# In[38]:

df3['percent_correct'] = df3['nright'].astype(float) / df3['ntotal']


# In[ ]:

## Make 'description' a feature wih important words mapped


# In[47]:

df3.columns


# In[50]:

df3.iloc[0]


# In[51]:

df3.iloc[0]['txt']


# In[52]:

df3.iloc[0]['description']


# In[69]:

for idx in range(100):
    print (df3.iloc[idx]['lesson'])
    print (df3.iloc[idx]['response'])


# In[100]:

my_val = (str(df3.iloc[0]['response']))
my_val = my_val.replace("': ","_")
my_val = my_val.replace("_{"," ")
my_val = my_val.replace("_[",", ")
for c in [']','[','{','}',"'",""]:
    my_val = my_val.replace(c,'')


# In[101]:

my_val


# In[95]:

str(df3.iloc[0]['response'])


# In[124]:

def stringify_response(resp):
    my_val = str(resp).replace("': ","_")
    my_val = my_val.replace("_{"," ")
    my_val = my_val.replace("_[",", ")
    for c in [']','[','{','}',"'","",","]:
        my_val = my_val.replace(c,'')
    return my_val


# In[125]:

stringify_response(df3.iloc[0]['response'])


# In[126]:

df3['response_str'] = df3['response'].apply(stringify_response)


# In[127]:

for idx in range(20):
    print (idx, df3['response_str'].iloc[idx])


# In[129]:

df3.columns


# In[131]:

df3.to_csv('data_frame_with_string_response.csv')


# In[132]:

df_lesson1.to_csv('lesson_summary.csv')


# In[ ]:



