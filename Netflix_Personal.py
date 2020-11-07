

"""
Name:               Karina Jonina 
Github:             https://github.com/kjonina/
Data Gathered:      based on Family Netflix Account
"""


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from io import StringIO # This is used for fast string concatination
import nltk # Use nltk for valid words
import collections as co # Need to make hash 'dictionaries' from nltk for fast processing
import warnings # current version of seaborn generates a bunch of warnings that we'll ignore
warnings.filterwarnings("ignore")
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer #Bag of Words



# The dataset used was collected from the following website:
# https://www.kaggle.com/shivamb/netflix-shows

# read the CSV file
dataset = pd.read_csv('ViewingActivity.csv')

# Will ensure that all columns are displayed
pd.set_option('display.max_columns', None) 

# prints out the top 5 values for the datasef
print(dataset.head())

# checking the dataset shape
print(dataset.shape)
# (6234, 12)


# prints out names of columns
print(dataset.columns)

# This tells us which variables are object, int64 and float 64. This would mean that 
# some of the object variables might have to be changed into a categorical variables and int64 to float64 
# depending on our analysis.
print(dataset.info())


# checking for missing data
dataset.isnull().sum() 

# dropping null value columns to avoid errors 
# You cant create a code to autofill the string data
dataset.dropna(inplace = True) 
#Profile Name                  0
#Start Time                    0
#Duration                      0
#Attributes                 6819
#Title                         0
#Supplemental Video Type    8224
#Device Type                   0
#Bookmark                      0
#Latest Bookmark               0
#Country                       0

# checking the dataset shape
print(dataset.shape)
# (10106, 10)



# =============================================================================
# Cleaning data
# =============================================================================
dataset = dataset.drop(['Attributes', 'Bookmark', 'Latest Bookmark'], axis = 1)

print(dataset.head())


# =============================================================================
# DataTime
# =============================================================================

dataset.dtypes

dataset['Profile Name'] = dataset['Profile Name'].astype('category')

dataset['Start Time'] = pd.to_datetime(dataset['Start Time'], utc = True)


dataset.head()


dataset['Duration'] = pd.to_timedelta(dataset['Duration'])

dataset['Duration'].groupby(dataset['Profile Name']).sum()
#Karina     90 days 06:56:55
#Karolina   21 days 22:49:48
#Kids        0 days 00:02:01
#Vit         4 days 07:36:39



# Examines the Profile Names 
plt.figure(figsize = (12, 8))
sns.countplot(x = 'Profile Name', data = dataset, palette = 'viridis', order = dataset['Profile Name'].value_counts().index)
plt.xticks(rotation = 90)
plt.title('Breakdown of Profile Name', fontsize = 16)
plt.ylabel('count', fontsize = 14)
plt.xlabel('Profile Name', fontsize = 14)
plt.show()

'''
Dad only recently started watching Netflix so a line graph with time would be more appropriate
Also: this just the number of times the user was logged on.
'''


# =============================================================================
# Creating Weekdays 
# =============================================================================

dataset['weekdays'] =  dataset['Start Time'].dt.weekday



dataset['weekdays'] = pd.Categorical(dataset['weekdays'], 
       categories = [0,1,2,3,4,5,6],
       ordered = True)


# find the table
dataset.groupby('Profile Name')['weekdays'].value_counts()


# Manual insertion of data. Is there a better way to do this?
new_dataset = pd.DataFrame({
    "Karina":[820,880,911,994,1187,1137,848],
    "Karolina":[304,243,289,295,234,562,960],
    "Vit":[80, 92, 92, 72, 125,121, 113]
    }, 
    index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", 'Sun']
)
dataset.plot(kind="bar")
plt.title("Netflix Consumption Study")
plt.xlabel("Family Member")
plt.ylabel("Neftlix")




# find the table
views_per_day = dataset.groupby(
        ['Profile Name', 'weekdays']
        )['Duration'].count().reset_index()


plotdata = views_per_day.pivot(index = 'Profile Name',
                                columns = 'weekdays',
                                values = 'Duration')

plotdata.plot(kind = 'bar')






# =============================================================================
# Creating Hour
# =============================================================================

dataset['hour'] = dataset['Start Time'].dt.hour

dataset['hour'] = pd.Categorical(dataset['hour'], 
       categories = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
       ordered = True)

# find the table
views_per_user = dataset.groupby(
        ['Profile Name', 'hour']
        )['Duration'].count().reset_index()


plotdata1 = views_per_user.pivot(index = 'Profile Name',
                                columns = 'hour',
                                values = 'Duration')

plotdata1.plot(kind = 'bar')

dataset.groupby('Profile Name')['hour'].value_counts()




Karina = dataset[dataset['Profile Name'] == 'Karina']

views_for_Karina = Karina.groupby(['hour'])['Duration'].count().reset_index()


views_for_Karina.plot(kind = 'bar')





Karolina = dataset[dataset['Profile Name'] == 'Karolina']

views_for_Karolina = Karolina.groupby(['hour'])['Duration'].count().reset_index()


views_for_Karolina.plot(kind = 'bar')





Vit = dataset[dataset['Profile Name'] == 'Vit']

views_for_Vit = Vit .groupby(['hour'])['Duration'].count().reset_index()


views_for_Vit .plot(kind = 'bar')
