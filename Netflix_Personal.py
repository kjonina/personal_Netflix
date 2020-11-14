

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
df = pd.read_csv('ViewingActihoury.csv')

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


# =============================================================================
# Creating Hour
# =============================================================================

df1['hour'] = df1['Start Time'].dt.hour

df1['hour'] = pd.Categorical(df1['hour'], 
       categories = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
       ordered = True)



# =============================================================================
# Creating separate datasets for Me
# =============================================================================

Karina = df1[df1['Profile Name'] == 'Karina']

# examining my hours spent on Netflix
Karina['Duration'].sum()

#'90 days 01:52:53'

# =============================================================================
# Checking Weekdays
# =============================================================================
# create the table
Karina['weekdays'].value_counts()

# create  the table
views_per_day = Karina.groupby(
        ['weekdays']
        )['Duration'].sum().reset_index()

print(views_per_day)
#  weekdays         Duration
#0      Mon 11 days 06:16:13
#1      Tue 11 days 01:22:45
#2      Wed 12 days 06:48:28
#3      Thu 13 days 02:25:43
#4      Fri 14 days 08:24:55
#5      Sat 15 days 13:01:07
#6      Sun 12 days 11:33:42


plt.figure(figsize = (12, 8))
views_per_day.plot(kind = 'bar')
plt.xticks(rotation = 90)
plt.title('Time spent on Netflix for each Weekday', fontsize = 14)
plt.ylabel('Duration', fontsize = 12)
plt.xlabel('Weekdays', fontsize = 12)
plt.show()


# =============================================================================
# Checking the hour of the day
# =============================================================================

# create the table
views_per_hour = df1.groupby(
        ['hour']
        )['Duration'].count().reset_index()

# generating the table
print(views_per_hour)

plt.figure(figsize = (12, 8))
views_per_hour.plot(kind = 'bar')
plt.xticks(rotation = 90)
plt.title('The amount of hours spend on each hour', fontsize = 14)
plt.ylabel('Duration', fontsize = 12)
plt.xlabel('Weekdays', fontsize = 12)
plt.show()



# =============================================================================
# Creating variable called Type: Tv Show or Movie
# =============================================================================

# trying to create the all the names with Season and create  a new variable called Type
Karina.loc[Karina['Title'].str.contains(': '), 'Type'] = 'TV Show'

# Trying to create  Movie in Type
Karina.loc[Karina['Type'].isnull(), 'Type'] = 'Movie'


# visualising duration and profile Name type
views_by_Type = Karina.groupby(
        ['Type']
        )['Duration'].sum().reset_index()


print(views_by_Type )
#       Type         Duration
# 0    Movie  8 days 00:12:30
# 1  TV Show 82 days 01:40:23


plt.figure(figsize = (12, 8))
views_by_Type.plot(kind = 'bar')
plt.xticks(rotation = 90)
plt.title('TV Show or Movie?', fontsize = 14)
plt.ylabel('Duration', fontsize = 12)
plt.show()



# =============================================================================
# Removing Seasons and Episodes from text in Titles
# =============================================================================

Karina['Title_name'] = (np.where(Karina['Title'].str.contains(': '),
                  Karina['Title'].str.split(':').str[0],
                  Karina['Title']))


# =============================================================================
# Examining dataset by Karina
# =============================================================================

#Creating the view of Karina's viewing habits
views_by_Karina = Karina.groupby(['Title_name', 'Type']
        )['Duration'].sum().sort_values(ascending = False)

# Viewing Karina's Top 50 most watched (in Duration) Tv Shows and Movies
views_by_Karina.head(20)

# Viewing Karina's Bottom 15 watched (in Duration) Tv Shows and Movies
views_by_Karina.tail(15)

#examining the shape of the data
print(views_by_Karina.shape)

# =============================================================================
# Splitting the Type by Movie and Tv Show
# =============================================================================
#splitting 
Karina_Movie = Karina[Karina['Type'] == 'Movie']
Karina_TV_Show = Karina[Karina['Type'] == 'TV Show']


# =============================================================================
# Examining Movies 
# =============================================================================

movie_views = Karina_Movie.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending = False)

top_movie = movie_views.head(15)


print(top_movie)
#Gone Girl                     09:40:01
#Gattaca                       06:08:54
#Pride & Prejudice             05:05:23
#Divergent                     04:39:50
#Wedding Crashers              04:34:33
#Inglourious Basterds          04:23:21
#The Maze Runner               04:16:24
#New Year's Eve                04:11:43
#Marriage Story                04:10:32
#P.S. I Love You               04:03:57
#He's Just Not That Into You   04:01:22
#The Break-Up                  03:58:16
#Baywatch                      03:35:24
#The Hangover                  03:19:22
#Leap Year                     03:12:29


#Creating a dataframe for Movie
top_move_df = pd.DataFrame(top_movie.head(15))
top_move_df.reset_index(inplace = True)
top_move_df.rename(columns={'index':'Title_name', 'Duration':'Duration'}, inplace = True)
top_move_df

#Creating a graph for Movie
movie_graph = sns.barplot(x = "Title_name", y = "Duration", data = top_move_df,
                 palette='Blues_d')
movie_graph.set_title('Top 15 Movies')
movie_graph.set_ylabel('Duration')
movie_graph.set_xlabel('Movies')
movie_graph.set_xticklabels(movie_graph.get_xticklabels(), rotation=90)



# =============================================================================
# Examining TV Show
# =============================================================================

TV_Show_view = Karina_TV_Show.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending = False)

top_TV_Show = TV_Show_view.head(15)

print(top_TV_Show)
#Gossip Girl                   7 days 10:16:19
#How I Met Your Mother         6 days 16:40:53
#Brooklyn Nine-Nine            6 days 07:05:39
#The Vampire Diaries           5 days 12:58:14
#How to Get Away With Murder   5 days 10:12:54
#Marvel's Jessica Jones        3 days 16:49:54
#Dynasty                       3 days 10:45:15
#iZombie                       2 days 22:24:23
#Money Heist                   2 days 22:14:52
#Sons of Anarchy               2 days 14:22:31
#Suits                         2 days 11:17:31
#House of Cards                2 days 00:56:52
#Riverdale                     1 days 22:06:32
#You                           1 days 20:28:53
#Spartacus                     1 days 17:06:22


#Creating a dataframe for TV Shows
top_TV_Show_df = pd.DataFrame(top_TV_Show.head(15))
top_TV_Show_df.reset_index(inplace = True)
top_TV_Show_df.rename(columns={'index':'Title_name', 'Duration':'Duration'}, inplace = True)
top_TV_Show_df

#Creating a graph for TV Shows
TV_Show_graph=sns.barplot(x = "Title_name", y = "Duration", data = top_move_df,
                 palette = 'Blues_d')
TV_Show_graph.set_title('Top 15 TV Shows')
TV_Show_graph.set_ylabel('Duration')
TV_Show_graph.set_xlabel('TV Shows')
TV_Show_graph.set_xticklabels(TV_Show_graph.get_xticklabels(), rotation = 90)




# =============================================================================
# 
# =============================================================================











'''
FUTURE RESEARCH IDEAS

Draw line graph with time + duration with 3 different lines for each hour

create  a snapshot of when the hours are all using Netflix

Analyse Titles

Run an algorythm to analyse who will watch which TV SHows and Movies with what titles?
'''


