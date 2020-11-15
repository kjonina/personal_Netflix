

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
import calendar
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

#creating a new variable called SVT where data is null or not null
df['SVT'] = df['Supplemental Video Type'].isnull()

# Trying to create  a dataset with only True as SVT
df = df[df.SVT == True]

#dropping unnecesary columns
df = df.drop(['SVT', 'Supplemental Video Type'], axis = 1)


# =============================================================================
# Correcting Variables Types
# =============================================================================

#changing Profile Name to a categorical variable
df['Profile Name'] = df['Profile Name'].astype('category')

# changing Start Time to Date Time in UTC Time Zone
df['Start Time'] = pd.to_datetime(df['Start Time'], utc = True)

# just getting the date
df['Date'] = df['Start Time'].dt.date

#Get the year
df['year'] = pd.DatetimeIndex(df['Date']).year

# get month name 
df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])

#creating variable month and year
df['month_year'] = pd.to_datetime(df['Date']).dt.to_period('M')

#changing Duration to time account
df['Duration'] = pd.to_timedelta(df['Duration'])


# =============================================================================
# Creating a Variable examining Pre-Covid and Covid
# =============================================================================
#Pre-Covid is before 12th March 2020 (That is the day that I was last in work)
df.loc[df['Date'] < datetime.date(2020,3,12), 'normality'] = 'Pre-Covid'
df.loc[df['Date'] > datetime.date(2020,3,12), 'normality'] = 'Covid'

df['normality'] = df['normality'].astype('category')


# =============================================================================
# Creating Weekdays 
# =============================================================================
# creating a weekday variable
df['weekdays'] =  df['Start Time'].dt.weekday


# making 'weekdays' a categorical variable
df['weekdays'] = pd.Categorical(df['weekdays'], 
       categories = [0,1,2,3,4,5,6],
       ordered = True)

# replacing 0-6 with Mon - Sun
df['weekdays'] = df['weekdays'].replace(0,'Mon')
df['weekdays'] = df['weekdays'].replace(1,'Tue')
df['weekdays'] = df['weekdays'].replace(2,'Wed')
df['weekdays'] = df['weekdays'].replace(3,'Thu')
df['weekdays'] = df['weekdays'].replace(4,'Fri')
df['weekdays'] = df['weekdays'].replace(5,'Sat')
df['weekdays'] = df['weekdays'].replace(6,'Sun')

#changing to category
df['weekdays'] = df['weekdays'].astype('category')

#reordering weekdays
df['weekdays'] = df['weekdays'].cat.reorder_categories(['Mon', 
   'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], ordered=True)


# =============================================================================
# Creating Hour
# =============================================================================

df['hour'] = df['Start Time'].dt.hour

df['hour'] = pd.Categorical(df['hour'], 
       categories = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
       ordered = True)

# =============================================================================
# Removing Seasons and Episodes from text in Titles
# =============================================================================

df['Title_name'] = (np.where(df['Title'].str.contains(': '),
                  df['Title'].str.split(':').str[0],
                  df['Title']))


# =============================================================================
# Creating variable called Type: Tv Show or Movie
# =============================================================================

# trying to create the all the names with Season and create  a new variable called Type
df.loc[df['Title'].str.contains(': '), 'Type'] = 'TV Show'

# Trying to create  Movie in Type
df.loc[df['Type'].isnull(), 'Type'] = 'Movie'

# =============================================================================
# Creating separate datasets (for Karina)
# =============================================================================

Karina = df[df['Profile Name'] == 'Karina']

# examining my hours spent on Netflix
Karina['Duration'].sum()

#'90 days 01:52:53'

#drop redundant Profile Name
Karina = Karina.drop(['Profile Name'], axis = 1)

# =============================================================================
# Analysing Weekdays (for Karina)
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
# Analysing the hour of the day (for Karina)
# =============================================================================

# create the table
views_per_hour = Karina.groupby(
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
# Analyse Date -> Year
# =============================================================================
# creating a year
Karina_Year = Karina.groupby(['year']
        )['Duration'].sum()

#Creating the table
print(Karina_Year)
#2018   37 days 07:59:17
#2019   28 days 13:46:35
#2020   24 days 04:07:01


Karina_Year_df = pd.DataFrame(Karina_Year)
Karina_Year_df.reset_index(inplace = True)
Karina_Year_df.rename(columns={'index':'year', 'Duration':'Duration'}, inplace = True)
Karina_Year_df

#Creating a graph for TV Shows
Karina_Year_df_graph=sns.barplot(x = "year", y = "Duration", data = Karina_Year_df,
                 palette = 'Blues_d')
Karina_Year_df_graph.set_title('Top 15 TV Shows Mid-Covid')
Karina_Year_df_graph.set_ylabel('Duration')
Karina_Year_df_graph.set_xlabel('TV Shows')
Karina_Year_df_graph.set_xticklabels(Karina_Year_df_graph.get_xticklabels(), rotation = 90)

# =============================================================================
# Analyse Date -> Month
# =============================================================================

# creating a month
Karina_Month = Karina.groupby(['month']
        )['Duration'].sum()

#printing a  table
print(Karina_Month)

Karina_Month_df = pd.DataFrame(Karina_Month)
Karina_Month_df.reset_index(inplace = True)
Karina_Month_df.rename(columns={'index':'month', 'Duration':'Duration'}, inplace = True)
Karina_Month_df

#Creating a graph for TV Shows
Karina_Month_df_graph=sns.barplot(x = "month", y = "Duration", data = Karina_Month_df,
                 palette = 'Blues_d')
Karina_Month_df_graph.set_title('Top 15 TV Shows Mid-Covid')
Karina_Month_df_graph.set_ylabel('Duration')
Karina_Month_df_graph.set_xlabel('TV Shows')
Karina_Month_df_graph.set_xticklabels(Karina_Month_df_graph.get_xticklabels(), rotation = 90)



# =============================================================================
# Analyse Date -> Month and Year
# =============================================================================
# creating a month and year
Karina_Month_Year = Karina.groupby(['month_year']
        )['Duration'].sum()

#printing a  table with months and years
print(Karina_Month_Year)


Karina_Month_Year_df = pd.DataFrame(Karina_Month_Year)
Karina_Month_Year_df.reset_index(inplace = True)
Karina_Month_Year_df.rename(columns={'index':'month_year', 'Duration':'Duration'}, inplace = True)
Karina_Month_Year_df

#Creating a graph for TV Shows
Karina_Month_Year_df_graph=sns.barplot(x = "month_year", y = "Duration", data = Karina_Month_Year_df,
                 palette = 'Greens_d')
Karina_Month_Year_df_graph.set_title('Top 15 TV Shows Mid-Covid')
Karina_Month_Year_df_graph.set_ylabel('Duration')
Karina_Month_Year_df_graph.set_xlabel('Month and Year')
Karina_Month_Year_df_graph.set_xticklabels(Karina_Month_Year_df_graph.get_xticklabels(), rotation = 90)



# =============================================================================
#  Analysing Type (for Karina)
# =============================================================================
# visualising duration and profile Name type
views_by_Type = Karina.groupby(
        ['Type']
        )['Duration'].sum().reset_index()


print(views_by_Type)
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
# Analsying dataset by Karina (for Karina)
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
# Splitting the Type by Movie and Tv Show (for Karina)
# =============================================================================
#splitting Movie and TV Show to create each dataset
Karina_Movie = Karina[Karina['Type'] == 'Movie']
Karina_TV_Show = Karina[Karina['Type'] == 'TV Show']


# =============================================================================
# Examining Movies (for Karina)
# =============================================================================

movie_views = Karina_Movie.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending = False)

#Creating Top 15
top_movie = movie_views.head(15)

#Printing Top 15
print(top_movie)

#Creating a dataframe for Movie
top_move_df = pd.DataFrame(top_movie.head(15))
top_move_df.reset_index(inplace = True)
top_move_df.rename(columns={'index':'Title_name', 'Duration':'Duration'}, inplace = True)


#Creating a graph for Movie
movie_graph = sns.barplot(x = "Title_name", y = "Duration", data = top_move_df,
                 palette='Blues_d')
movie_graph.set_title('Top 15 Movies')
movie_graph.set_ylabel('Duration')
movie_graph.set_xlabel('Movies')
movie_graph.set_xticklabels(movie_graph.get_xticklabels(), rotation=90)



# =============================================================================
# Examining TV Show (for Karina)
# =============================================================================

TV_Show_view = Karina_TV_Show.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending = False)
#Creating Top 15
top_TV_Show = TV_Show_view.head(15)

#Printing Top 15
print(top_TV_Show)



#Creating a dataframe for TV Shows
top_TV_Show_df = pd.DataFrame(top_TV_Show)
top_TV_Show_df.reset_index(inplace = True)
top_TV_Show_df.rename(columns={'index':'Title_name', 'Duration':'Duration'}, inplace = True)
top_TV_Show_df

#Creating a graph for TV Shows
TV_Show_graph=sns.barplot(x = "Title_name", y = "Duration", data = top_TV_Show_df,
                 palette = 'Blues_d')
TV_Show_graph.set_title('Top 15 TV Shows')
TV_Show_graph.set_ylabel('Duration')
TV_Show_graph.set_xlabel('TV Shows')
TV_Show_graph.set_xticklabels(TV_Show_graph.get_xticklabels(), rotation = 90)



# =============================================================================
# Analysing Pre-Covid and Covid Viewing Habits (for Karina)
# =============================================================================
# Analyse data

comparing_habits = pd.DataFrame({'Normality': Karina['normality'],
                   'Hour': Karina['hour'],
                   'Weekdays': Karina['weekdays'],
                   'Duration': Karina['Duration']})
    
comparing_habits_WD_pivot = pd.pivot_table(
        comparing_habits, values='Duration', index=['Weekdays'], columns=['Normality'], aggfunc=np.sum)

# Compare the data
print(comparing_habits_WD_pivot)
#A             Covid        Pre-Covid
#C                                   
#Mon 1 days 19:27:22  9 days 10:48:51
#Tue 2 days 14:34:10  8 days 10:48:35
#Wed 2 days 12:23:10  9 days 18:25:18
#Thu 3 days 15:22:07  9 days 10:45:32
#Fri 3 days 20:37:57 10 days 11:46:58
#Sat 3 days 03:23:11 12 days 09:37:56
#Sun 2 days 04:03:42 10 days 07:30:00


plt.figure(figsize = (12, 8))
comparing_habits_WD_pivot.plot(kind = 'bar')
plt.xticks(rotation = 90)
plt.title('Viewing Habits for Weekday', fontsize = 14)
plt.ylabel('Duration', fontsize = 12)
plt.xlabel('Weekdays', fontsize = 12)
plt.show()


comparing_habits_HRS_pivot = pd.pivot_table(
        comparing_habits, values='Duration', index=['Hour'], columns=['Normality'], aggfunc=np.sum)

# Compare the data
print(comparing_habits_HRS_pivot)
#Normality           Covid        Pre-Covid
#Hour                                      
#0         0 days 14:45:57  5 days 10:59:59
#1         0 days 09:06:41  3 days 04:25:16
#2         0 days 02:42:58  2 days 09:18:18
#3         0 days 01:37:58  1 days 18:11:27
#4         0 days 03:28:09  1 days 06:26:35
#5         0 days 05:21:30  1 days 01:15:49
#6         0 days 09:19:23  0 days 18:18:09
#7         0 days 12:16:01  1 days 08:16:58
#8         0 days 18:31:23  1 days 09:01:39
#9         0 days 16:12:53  1 days 05:47:19
#10        0 days 15:10:08  1 days 08:13:29
#11        0 days 21:10:02  0 days 23:12:02
#12        1 days 01:16:07  1 days 05:41:01
#13        0 days 21:12:53  1 days 05:33:17
#14        0 days 21:04:03  1 days 00:32:54
#15        1 days 02:54:27  1 days 07:21:45
#16        0 days 22:16:19  1 days 18:21:33
#17        1 days 02:27:45  2 days 09:55:51
#18        0 days 17:25:27  3 days 00:14:31
#19        1 days 03:55:54  3 days 04:23:37
#20        0 days 21:47:21  5 days 01:30:09
#21        2 days 05:00:52  8 days 12:16:28
#22        2 days 02:09:37 10 days 11:48:08
#23        1 days 06:37:51  8 days 22:36:56


plt.figure(figsize = (12, 8))
comparing_habits_HRS_pivot.plot(kind = 'bar')
plt.xticks(rotation = 90)
plt.title('Viewing Habits for Hour of Day', fontsize = 14)
plt.ylabel('Duration', fontsize = 12)
plt.xlabel('Hour of day', fontsize = 12)
plt.show()


# =============================================================================
# Split Covid by Movie and TV Show (for Karina)
# =============================================================================
Pre_Covid_Movie = Karina_Movie[Karina_Movie['normality'] == 'Pre-Covid']
Pre_Covid_TV_Show= Karina_TV_Show[Karina_TV_Show['normality'] == 'Pre-Covid']


Covid_Movie = Karina_Movie[Karina_Movie['normality'] == 'Covid']
Covid_TV_Show = Karina_TV_Show[Karina_TV_Show['normality'] == 'Covid']

# =============================================================================
# COVID TV SHOW LIST (for Karina)
# =============================================================================
# creating a table for Covid Viewing of TV Shows
Covid_TV_Show_view = Covid_TV_Show.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending = False)


top_TV_Show_mid_COVID = Covid_TV_Show_view.head(15)

# checking viewing after 12th Mardch 2020
print(top_TV_Show_mid_COVID)
#How I Met Your Mother                 2 days 23:28:32
#How to Get Away With Murder           2 days 04:09:05
#Once Upon a Time                      1 days 09:30:18
#Riverdale                             1 days 08:01:11
#Brooklyn Nine-Nine                    1 days 03:16:51
#Good Girls                            0 days 23:52:32
#Gossip Girl                           0 days 22:41:50
#The Fall                              0 days 21:42:41
#The Innocence Files                   0 days 13:53:50
#Inside the World’s Toughest Prisons   0 days 11:12:47
#You                                   0 days 10:43:28
#Unsolved Mysteries                    0 days 10:00:02
#Conversations with a Killer           0 days 09:11:02
#Emily in Paris                        0 days 06:55:21
#Money Heist                           0 days 06:18:53

#Creating a dataframe for TV Shows
top_TV_Show_mid_COVID_df = pd.DataFrame(top_TV_Show_mid_COVID.head(15))
top_TV_Show_mid_COVID_df.reset_index(inplace = True)
top_TV_Show_mid_COVID_df.rename(columns={'index':'Title_name', 'Duration':'Duration'}, inplace = True)
top_TV_Show_mid_COVID_df

#Creating a graph for TV Shows
top_TV_Show_mid_COVID_graph=sns.barplot(x = "Title_name", y = "Duration", data = top_TV_Show_mid_COVID_df,
                 palette = 'Blues_d')
top_TV_Show_mid_COVID_graph.set_title('Top 15 TV Shows Mid-Covid')
top_TV_Show_mid_COVID_graph.set_ylabel('Duration')
top_TV_Show_mid_COVID_graph.set_xlabel('TV Shows')
top_TV_Show_mid_COVID_graph.set_xticklabels(top_TV_Show_mid_COVID_graph.get_xticklabels(), rotation = 90)


# =============================================================================
# COVID MOVIES LIST (for Karina)
# =============================================================================

Covid_movie_views = Covid_Movie.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending = False)

Covid_top_movie = Covid_movie_views.head(15)


print(Covid_top_movie)

#The Break-Up                   03:58:16
#Gone Girl                      03:05:51
#Wedding Crashers               02:51:50
#Holidate                       02:51:19
#The Five-Year Engagement       02:46:19
#Spenser Confidential           02:43:48
#Sex and the City 2             02:27:50
#The Old Guard                  02:17:05
#Love Wedding Repeat            02:14:33
#Love, Guaranteed               02:06:09
#Marriage Story                 02:03:47
#How to Lose a Guy in 10 Days   02:01:14
#Anna Karenina                  02:00:40
#He's Just Not That Into You    02:00:09
#Think Like a Man               01:54:18


#Creating a dataframe for Movie
Covid_top_move_df = pd.DataFrame(Covid_top_movie)
Covid_top_move_df.reset_index(inplace = True)
Covid_top_move_df.rename(columns={'index':'Title_name', 'Duration':'Duration'}, inplace = True)
Covid_top_move_df

#Creating a graph for Movie
Covid_top_move_mid_COVID_graph=sns.barplot(x = "Title_name", y = "Duration", data = Covid_top_move_df,
                 palette = 'Blues_d')
Covid_top_move_mid_COVID_graph.set_title('Top Movie Mid-Covid')
Covid_top_move_mid_COVID_graph.set_ylabel('Duration')
Covid_top_move_mid_COVID_graph.set_xlabel('Movie')
Covid_top_move_mid_COVID_graph.set_xticklabels(Covid_top_move_mid_COVID_graph.get_xticklabels(), rotation = 90)




