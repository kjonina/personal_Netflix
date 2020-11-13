

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



# The df used was collected from the following website:
# https://www.kaggle.com/shivamb/netflix-shows

# read the CSV file
df = pd.read_csv('ViewingActivity.csv')

# Will ensure that all columns are displayed
pd.set_option('display.max_columns', None) 

# prints out the top 5 values for the datasef
print(df.head())

# checking the df shape
print(df.shape)
# (6234, 12)


# prints out names of columns
print(df.columns)

# This tells us which variables are object, int64 and float 64. This would mean that 
# some of the object variables might have to be changed into a categorical variables and int64 to float64 
# depending on our analysis.
print(df.info())


# checking for missing data
df.isnull().sum() 
#Profileame N                  0
#Start Time                    0
#Duration                      0
#Attributes                 6819
#Title                         0
#Supplemental Video Type    8224
#Device Type                   0
#Bookmark                      0
#Latest Bookmark               0
#Country                       0




# checking the df shape
print(df.shape)
# (10106, 10)



# =============================================================================
# Droping Columns
# =============================================================================
df = df.drop(['Attributes', 'Bookmark', 'Latest Bookmark', 'Country', 'Device Type'], axis = 1)

print(df.head())

df['SVT'] = df['Supplemental Video Type'].isnull()

# Trying to create a dataset with only True as SVT
df1 = df[df.SVT == True]
df1 = df1.drop(['SVT', 'Supplemental Video Type'], axis = 1)


# =============================================================================
# DataTime
# =============================================================================
#checking data types
df1.dtypes

#changing Profile Name to a categorical variable
df1['Profile Name'] = df1['Profile Name'].astype('category')

# changing Start Time to Date Time in UTC Time Zone
df1['Start Time'] = pd.to_datetime(df1['Start Time'], utc = True)


df1.head()

#changing Duration to time account
df1['Duration'] = pd.to_timedelta(df1['Duration'])

# examining individual users hours spent on Netflix
df1['Duration'].groupby(df1['Profile Name']).sum()

#Profile Name
#Karina     90 days 01:52:53
#Karolina   21 days 17:37:15
#Vit         4 days 06:26:10



# Examines the Profile Names 
plt.figure(figsize = (12, 8))
sns.countplot(x = 'Profile Name', data = df1, palette = 'viridis', order = df1['Profile Name'].value_counts().index)
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
# creating a weekday variable
df1['weekdays'] =  df1['Start Time'].dt.weekday


# making 'weekdays' a categorical variable
df1['weekdays'] = pd.Categorical(df1['weekdays'], 
       categories = [0,1,2,3,4,5,6],
       ordered = True)



# find the table
df1.groupby('Profile Name')['weekdays'].value_counts()


# Manual insertion of data. Is there a better way to do this?
new_df1 = pd.DataFrame({
    "Karina":[820,880,911,994,1187,1137,848],
    "Karolina":[304,243,289,295,234,562,960],
    "Vit":[80, 92, 92, 72, 125,121, 113]
    }, 
    index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", 'Sun']
)
new_df1.plot(kind="bar")
plt.title("Netflix Consumption Study")
plt.xlabel("Family Member")
plt.ylabel("Neftlix")




# find the table
views_per_day = df1.groupby(
        ['Profile Name', 'weekdays']
        )['Duration'].sum().reset_index()


plotdata = views_per_day.pivot(index = 'weekdays',
                                columns = 'Profile Name',
                                values = 'Duration')

plotdata.plot(kind = 'bar')






# =============================================================================
# Creating Hour
# =============================================================================

df1['hour'] = df1['Start Time'].dt.hour

df1['hour'] = pd.Categorical(df1['hour'], 
       categories = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
       ordered = True)

# find the table
views_per_user = df1.groupby(
        ['Profile Name', 'hour']
        )['Duration'].count().reset_index()


plotdata1 = views_per_user.pivot(index = 'Profile Name',
                                columns = 'hour',
                                values = 'Duration')

plotdata1.plot(kind = 'bar')

df1.groupby('Profile Name')['hour'].value_counts()

# =============================================================================
# Creating Type: Tv Show or Movie
# =============================================================================

#trying to find the all the names with Season and create a new variable called Type
df1.loc[df1['Title'].str.contains('Season'), 'Type'] = 'TV Show'

#Trying to create Movie in Type
df1.loc[df1['Type'].isnull(), 'Type'] = 'Movie'


#visualising duration and profile Name type
views_per_user_by_Type = df1.groupby(
        ['Profile Name', 'Type']
        )['Duration'].sum().reset_index()

#Creating table to view Duration by Name and Type
pivot_movie_name = pd.DataFrame({'A': df1['Profile Name'],
                   'B': df1['Type'],
                   'C': df1['Duration']})

# Pivoting the talbe
pivot_movie_name = pd.pivot_table(pivot_movie_name, values='C', index=['A'], columns=['B'], aggfunc='sum')

#Produce the table
print(pivot_movie_name)
#B                   Movie          TV Show
#A                                         
#Karina   22 days 03:48:58 67 days 22:03:55
#Karolina 10 days 04:41:23 11 days 12:55:52
#Vit       1 days 10:28:40  2 days 19:57:30

plotdata2 = views_per_user_by_Type.pivot(index = 'Profile Name',
                                columns = 'Type',
                                values = 'Duration')

plotdata2.plot(kind = 'bar')

# =============================================================================
# Splitting Titles
# =============================================================================


for title in df.Title:
    title_name = []
    if df[df['Title'].str.contains('Season', regex=False)]:
        df['Title'].lsplit('; ')
        title_name.append(str(df['Title']).lstrip(' :'))
return title_name




if df[df['Title'].any().contains('Season', regex=False)]:
df['Title'].lsplit('; ')


seasons = df1[df1['Title'].str.contains('Season', regex=False)]



def remove_title(text):
        clean_Title = [word for word in text.split() if text.str.contains('Sason')]
        return clean_Title

df1['Title_Name']=df1['Title'].apply(remove_title)