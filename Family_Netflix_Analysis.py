

"""
Name:               Karina Jonina 
Github:             https://github.com/kjonina/
Data Gathered:      based on Family Netflix Account
Inspired by:        https://www.dataquest.io/blog/python-tutorial-analyze-personal-netflix-data/
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
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer #Bag of Words

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

#creating a new variable called SVT where data is null or not null
df['SVT'] = df['Supplemental Video Type'].isnull()

# Trying to create  a dataset with only True as SVT
df1 = df[df.SVT == True]

#dropping unnecesary columns
df1 = df1.drop(['SVT', 'Supplemental Video Type'], axis = 1)


# =============================================================================
# Correcting Variables Types
# =============================================================================
#checking data types
df1.dtypes

#changing Profile Name to a categorical variable
df1['Profile Name'] = df1['Profile Name'].astype('category')

# changing Start Time to Date Time in UTC Time Zone
df1['Start Time'] = pd.to_datetime(df1['Start Time'], utc = True)

#changing Duration to time account
df1['Duration'] = pd.to_timedelta(df1['Duration'])

# examining individual Vits hours spent on Netflix
df1['Duration'].groupby(df1['Profile Name']).sum()

#Profile Name
#Karina     90 days 01:52:53
#Karolina   21 days 17:37:15
#Vit3         4 days 06:26:10


''' FIx graph '''
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
Also: this just the number of times the Vit was logged on.
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

# replacing 0-6 with Mon - Sun
df1['weekdays'] = df1['weekdays'].replace(0,'Mon')
df1['weekdays'] = df1['weekdays'].replace(1,'Tue')
df1['weekdays'] = df1['weekdays'].replace(2,'Wed')
df1['weekdays'] = df1['weekdays'].replace(3,'Thu')
df1['weekdays'] = df1['weekdays'].replace(4,'Fri')
df1['weekdays'] = df1['weekdays'].replace(5,'Sat')
df1['weekdays'] = df1['weekdays'].replace(6,'Sun')

#changing to category
df1['weekdays'] = df1['weekdays'].astype('category')

#reordering weekdays
df1['weekdays'] = df1['weekdays'].cat.reorder_categories(['Mon', 
   'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], ordered=True)


# create the table
df1.groupby('Profile Name')['weekdays'].value_counts()

# create  the table
views_per_day = df1.groupby(
        ['Profile Name', 'weekdays']
        )['Duration'].sum().reset_index()


plotdata = views_per_day.pivot(index = 'weekdays',
                                columns = 'Profile Name',
                                values = 'Duration')
plt.figure(figsize = (12, 8))
plotdata.plot(kind = 'bar')
plt.xticks(rotation = 90)
plt.title('Time spent on Netflix for each Weekday', fontsize = 14)
plt.ylabel('Duration', fontsize = 12)
plt.xlabel('Weekdays', fontsize = 12)
plt.show()






# =============================================================================
# Creating Hour
# =============================================================================

df1['hour'] = df1['Start Time'].dt.hour

df1['hour'] = pd.Categorical(df1['hour'], 
       categories = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
       ordered = True)

# create the table
views_per_Vit = df1.groupby(
        ['Profile Name', 'hour']
        )['Duration'].count().reset_index()


plotdata1 = views_per_Vit.pivot(index = 'Profile Name',
                                columns = 'hour',
                                values = 'Duration')

plotdata1.plot(kind = 'bar')

df1.groupby('Profile Name')['hour'].value_counts()

# =============================================================================
# Creating variable called Type: Tv Show or Movie
# =============================================================================

#trying to create the all the names with Season and create  a new variable called Type
df1.loc[df1['Title'].str.contains(': '), 'Type'] = 'TV Show'

#Trying to create  Movie in Type
df1.loc[df1['Type'].isnull(), 'Type'] = 'Movie'


#visualising duration and profile Name type
views_per_Vit_by_Type = df1.groupby(
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
#Vit3       1 days 10:28:40  2 days 19:57:30

plotdata2 = views_per_Vit_by_Type.pivot(index = 'Profile Name',
                                columns = 'Type',
                                values = 'Duration')


plt.figure(figsize = (12, 8))
plotdata2.plot(kind = 'bar')
plt.xticks(rotation = 90)
plt.title('TV Show or Movie?', fontsize = 14)
plt.ylabel('Duration', fontsize = 12)
plt.show()



# =============================================================================
# Removing Seasons and Episodes from text in Titles
# =============================================================================

df1['Title_name'] = (np.where(df1['Title'].str.contains(': '),
                  df1['Title'].str.split(':').str[0],
                  df1['Title']))


views_by_Title_name = df1.groupby(['Title_name']
        )['Duration'].sum().reset_index()


# =============================================================================
# Duration by Profile Name and Titles
# =============================================================================
#visualising duration by profile Name and title
views_by_Title_name = df1.groupby(
        ['Title_name']
        )['Duration'].sum().sort_values(ascending=False)

#Creating table to view Duration by Name and title
pivot_title_name = pd.DataFrame({'A': df1['Profile Name'],
                   'B': df1['Title_name'],
                   'C': df1['Duration']})

# Pivoting the table
pivot_title_name1 = pd.pivot_table(pivot_title_name, values='C', index=['B'], columns=['A'], aggfunc='sum')

#Produce the table
print(pivot_title_name1)


# =============================================================================
# Creating separate datasets for each Vit to analyse Top Movies and TV Shows for each Vit
# =============================================================================

Karina = df1[df1['Profile Name'] == 'Karina']

Karolina = df1[df1['Profile Name'] == 'Karolina']

Vit3 = df1[df1['Profile Name'] == 'Vit3']


# =============================================================================
# Examining dataset by Karina
# =============================================================================

# create  the table
views_Karina_per_hour = Karina.groupby(
        ['hour']
        )['Duration'].count().reset_index()

#plotting the table
views_Karina_per_hour.plot()


# create  the table
views_Karina_per_day = Karina.groupby(
        ['weekdays']
        )['Duration'].sum().reset_index()

#plotting the table
views_Karina_per_day.plot()


#Creating the view of Karina's viewing habits
views_by_Karina = Karina.groupby(['Title_name', 'Type']
        )['Duration'].sum().sort_values(ascending=False)

# Viewing Karina's Top 50 most watched (in Duration) Tv Shows and Movies
views_by_Karina.head(20)

# Viewing Karina's Bottom 15 watched (in Duration) Tv Shows and Movies
views_by_Karina.tail(15)


#examining the shape of the data
print(views_by_Karina.shape)

#Too much data so it needs to be split by Movie and Tv Show

Karina_Movie = Karina[Karina['Type'] == 'Movie']
Karina_TV_Show = Karina[Karina['Type'] == 'TV Show']

#Creating the view of Karina's viewing habits By Movie
movie_views_by_Karina = Karina_Movie.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending=False)

# Viewing Karina's Top 50 most watched (in Duration) Movies
movie_views_by_Karina.head(15)

# Viewing Karina's Bottom 15 watched (in Duration) Movies
movie_views_by_Karina.tail(15)


#Creating the view of Karina's viewing habits By TV Shows
TV_Shows_views_by_Karina = Karina_TV_Show.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending=False)

# Viewing Karina's Top 15 most watched (in Duration) Tv Shows 
TV_Shows_views_by_Karina.head(15)

# Viewing Karina's Bottom 15 watched (in Duration) Tv Shows 
TV_Shows_views_by_Karina.tail(15)


# =============================================================================
# Examining dataset by Karolina
# =============================================================================
Karolina['Title_name'].unique()

# Examining the most clicks
Karolina.groupby(['Title_name']).size().sort_values(ascending=False)


# create the table
views_Karolina = Karolina.groupby(
        ['hour']
        )['Duration'].count().reset_index()




#Creating the view of Karolina's viewing habits
views_by_Karolina = Karolina.groupby(['Title_name', 'Type']
        )['Duration'].sum().sort_values(ascending=False)

# Viewing Karolina's Top 50 most watched (in Duration) Tv Shows and Movies
views_by_Karolina.head(50)

# Viewing Karolina's Bottom 15 watched (in Duration) Tv Shows and Movies
views_by_Karolina.tail(15)

#examining the shape of the data
print(views_by_Karolina.shape)



#Too much data so it needs to be split by Movie and Tv Show

Karolina_Movie = Karolina[Karolina['Type'] == 'Movie']
Karolina_TV_Show = Karolina[Karolina['Type'] == 'TV Show']

#Creating the view of Karolina's viewing habits By Movie
movie_views_by_Karolina = Karolina_Movie.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending=False)

# Viewing Karolina's Top 50 most watched (in Duration) Movies
movie_views_by_Karolina.head(50)

# Viewing Karolina's Bottom 15 watched (in Duration)  Movies
movie_views_by_Karolina.tail(15)


#Creating the view of Karolina's viewing habits By TV Shows
TV_Shows_views_by_Karolina = Karolina_TV_Show.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending=False)

# Viewing Karolina's Top 50 most watched (in Duration) Tv Shows
TV_Shows_views_by_Karolina.head(50)

# Viewing Karolina's Bottom 15 watched (in Duration) Tv Shows 
TV_Shows_views_by_Karolina.tail(15)


# =============================================================================
# Examining dataset by Vit3
# =============================================================================

#Creating the view of Vit3's viewing habits
views_by_Vit3 = Vit3.groupby(
        ['Title_name', 'Type']
        )['Duration'].sum().sort_values(ascending=False)

# Viewing Vit3's Top 50 most watched (in Duration) Tv Shows and Movies
views_by_Vit3.head(50)

# Viewing Karolina's Bottom 15 watched (in Duration) Tv Shows and Movies
views_by_Vit3.tail(15)

#examining the shape of the data
print(views_by_Vit3.shape)


'''
FUTURE RESEARCH IDEAS

Draw line graph with time + duration with 3 different lines for each Vit

create  a snapshot of when the Vits are all using Netflix

Analyse Titles

Run an algorythm to analyse who will watch which TV SHows and Movies with what titles?
'''


