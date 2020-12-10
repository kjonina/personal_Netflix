

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

# This tells us which variables are object, int64 and float 64. 
print(df.info())

# checking for missing data
df.isnull().sum() 

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
df['date'] = df['Start Time'].dt.date

#Get the year
df['year'] = pd.DatetimeIndex(df['date']).year

# get month name 
#df['month'] = df['date'].apply(lambda x: calendar.month_abbr[x])

#creating variable month and year
df['month_year'] = pd.to_datetime(df['date']).dt.to_period('M')

#changing Duration to time account
df['Duration'] = pd.to_timedelta(df['Duration'])


# =============================================================================
# Creating a Variable examining Pre-Covid and Covid
# =============================================================================
#Pre-Covid is before 12th March 2020 (That is the day that I was last in work)
df.loc[df['date'] < datetime.date(2020,3,12), 'normality'] = 'Pre-Covid'
df.loc[df['date'] > datetime.date(2020,3,12), 'normality'] = 'Covid'

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

views_per_day_df = pd.DataFrame(views_per_day)
views_per_day_df.reset_index()
views_per_day_df.rename(columns = {'index':'weekdays', 'Duration':'Duration'}, inplace = True)
views_per_day_df



sns.set()
#Creating a graph for Month and Year
plt.figure(figsize = (12, 8))
views_per_day_df_graph = sns.barplot(x = "weekdays", y = "Duration", data = views_per_day_df,
                 palette = 'magma')
views_per_day_df_graph.set_title('Time spent on Netflix for each Weekday', fontsize = 20)
views_per_day_df_graph.set_ylabel('Duration',fontsize = 14)
views_per_day_df_graph.set_xlabel('Month and Year', fontsize = 14)
views_per_day_df_graph.set_xticklabels(views_per_day_df_graph.get_xticklabels())


#Save the graph
views_per_day_df_graph.figure.savefig('views_per_day_df_graph.png')

# =============================================================================
# Analysing the hour of the day (for Karina)
# =============================================================================

# create the table
views_per_hour = Karina.groupby(
        ['hour']
        )['Duration'].sum().reset_index()

# generating the table
print(views_per_hour)

views_per_hour_df = pd.DataFrame(views_per_hour)
views_per_hour_df.reset_index()
views_per_hour_df.rename(columns = {'index':'hour', 'Duration':'Duration'}, inplace = True)
views_per_hour_df

#Creating a graph for Month and Year
plt.figure(figsize = (12, 8))
views_per_hour_df_graph = sns.barplot(x = "hour", y = "Duration", data = views_per_hour_df,
                 palette = 'magma')
views_per_hour_df_graph.set_title('Top 15 TV Shows Mid-Covid', fontsize = 20)
views_per_hour_df_graph.set_ylabel('Duration', fontsize = 14)
views_per_hour_df_graph.set_xlabel('Month and Year', fontsize = 14)
views_per_hour_df_graph.set_xticklabels(views_per_hour_df_graph.get_xticklabels(), rotation = 90)


#Save the graph
views_per_hour_df_graph.figure.savefig('views_per_hour_df_graph.png')


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
Karina_Year_df.rename(columns = {'index':'year', 'Duration':'Duration'}, inplace = True)
Karina_Year_df

#Creating a graph for TV Shows
plt.figure(figsize = (12, 8))
Karina_Year_df_graph = sns.barplot(x = "year", y = "Duration", data = Karina_Year_df,
                 palette = 'Blues_d')
Karina_Year_df_graph.set_title('Which year did I watch the most Netflix?', fontsize = 20)
Karina_Year_df_graph.set_ylabel('Duration', fontsize = 14)
Karina_Year_df_graph.set_xlabel('Year', fontsize = 14)
Karina_Year_df_graph.set_xticklabels(Karina_Year_df_graph.get_xticklabels(), rotation = 90)

#Save the graph
Karina_Year_df_graph.figure.savefig('Karina_Year_df_graph.png')


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
Karina_Month_df.rename(columns = {'index':'month', 'Duration':'Duration'}, inplace = True)
Karina_Month_df

#Creating a graph for TV Shows
plt.figure(figsize = (12, 8))
Karina_Month_df_graph = sns.barplot(x = "month", y = "Duration", data = Karina_Month_df,
                 palette = 'Blues_d')
Karina_Month_df_graph.set_title('Which month did I watch the most Netflix?', fontsize = 20)
Karina_Month_df_graph.set_ylabel('Duration', fontsize = 14)
Karina_Month_df_graph.set_xlabel('Month', fontsize = 14)
Karina_Month_df_graph.set_xticklabels(Karina_Month_df_graph.get_xticklabels(), rotation = 90)

#Save the graph
Karina_Month_df_graph.figure.savefig('Karina_Month_df_graph.png')


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
Karina_Month_Year_df.rename(columns = {'index':'month_year', 'Duration':'Duration'}, inplace = True)
Karina_Month_Year_df

#Creating a graph for Month and Year
plt.figure(figsize = (12, 8))
Karina_Month_Year_df_graph = sns.barplot(x = "month_year", y = "Duration", data = Karina_Month_Year_df,
                 palette = 'Greens_d')
Karina_Month_Year_df_graph.set_title('When did I watch most Netflix?', fontsize = 20)
Karina_Month_Year_df_graph.set_ylabel('Duration', fontsize = 14)
Karina_Month_Year_df_graph.set_xlabel('Month and Year', fontsize = 14)
Karina_Month_Year_df_graph.set_xticklabels(Karina_Month_Year_df_graph.get_xticklabels(), rotation = 90)

#Save the graph
Karina_Month_Year_df_graph.figure.savefig('Karina_Month_Year_df_graph.png')



# =============================================================================
#  Analysing Type (for Karina)
# =============================================================================
# visualising duration and profile Name type
views_by_Type = Karina.groupby(
        ['Type']
        )['Duration'].sum().reset_index()


print(views_by_Type)

#Creating a dataframe for TV Shows
views_by_Type_df = pd.DataFrame(views_by_Type)
views_by_Type_df.reset_index()
views_by_Type_df.rename(columns = {'index':'Type', 'Duration':'Duration'}, inplace = True)
views_by_Type_df

#Creating a 
plt.figure(figsize = (12, 8))
views_by_Type_df_graph = sns.barplot(x = "Type", y = "Duration", data = views_by_Type_df,
                 palette = 'mako')
views_by_Type_df_graph.set_title('Movie or TV Show?', fontsize = 20)
views_by_Type_df_graph.set_ylabel('Duration', fontsize = 14)
views_by_Type_df_graph.set_xlabel('Month and Year', fontsize = 14)
views_by_Type_df_graph.set_xticklabels(views_by_Type_df_graph.get_xticklabels())

#Save the graph
views_by_Type_df_graph.figure.savefig('views_by_Type_df_graph.png')



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
top_move_df.rename(columns = {'index':'Title_name', 'Duration':'Duration'}, inplace = True)


#Creating a graph for Movie
plt.figure(figsize = (12, 8))
movie_graph = sns.barplot(y = "Title_name", x = "Duration", data = top_move_df,
                 palette = 'viridis')
movie_graph.set_title('Top 15 Movies', fontsize = 20)
movie_graph.set_ylabel('Duration', fontsize = 14)
movie_graph.set_xlabel('Movies', fontsize = 14)
movie_graph.set_xticklabels(movie_graph.get_xticklabels(), rotation = 90)

#Save the graph
movie_graph.figure.savefig('movie_graph.png')

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
top_TV_Show_df.rename(columns = {'index':'Title_name', 'Duration':'Duration'}, inplace = True)
top_TV_Show_df

#Creating a graph for TV Shows
plt.figure(figsize = (12, 8))
TV_Show_graph = sns.barplot(y = "Title_name", x = "Duration", data = top_TV_Show_df,
                 palette = 'viridis')
TV_Show_graph.set_title('Top 15 TV Shows', fontsize = 20)
TV_Show_graph.set_ylabel('TV Shows', fontsize = 14)
TV_Show_graph.set_xlabel('Duration', fontsize = 14)
TV_Show_graph.set_xticklabels(TV_Show_graph.get_xticklabels(), rotation = 90)

#Save the graph
TV_Show_graph.figure.savefig('TV_Show_graph.png')



# =============================================================================
# Analysing Pre-Covid and Covid Viewing Habits (for Karina)
# =============================================================================
# Analyse data

comparing_habits = pd.DataFrame({'Normality': Karina['normality'],
                   'Hour': Karina['hour'],
                   'Weekdays': Karina['weekdays'],
                   'Duration': Karina['Duration']})
    
comparing_habits_WD_pivot = pd.pivot_table(
        comparing_habits, values='Duration', index = ['Weekdays'], columns = ['Normality'], aggfunc = np.sum)

# Compare the data
print(comparing_habits_WD_pivot)

comparing_habits_WD_pivot.plot(kind = 'bar', figsize=(12,8))
plt.xticks(rotation = 90)
plt.title('Viewing Habits for Weekday', fontsize = 14)
plt.ylabel('Duration', fontsize = 12)
plt.xlabel('Weekdays', fontsize = 12)
plt.show()


comparing_habits_HRS_pivot = pd.pivot_table(
        comparing_habits, values = 'Duration', index = ['Hour'], columns = ['Normality'], aggfunc = np.sum)

# Compare the data
print(comparing_habits_HRS_pivot)

comparing_habits_HRS_pivot.plot(kind = 'bar', figsize=(12,8))
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

#Creating a dataframe for TV Shows
top_TV_Show_mid_COVID_df = pd.DataFrame(top_TV_Show_mid_COVID.head(15))
top_TV_Show_mid_COVID_df.reset_index(inplace = True)
top_TV_Show_mid_COVID_df.rename(columns = {'index':'Title_name', 'Duration':'Duration'}, inplace = True)
top_TV_Show_mid_COVID_df


#Creating a graph for TV Shows
plt.figure(figsize = (12, 8))
top_TV_Show_mid_COVID_graph = sns.barplot(y = "Title_name", x = "Duration", data = top_TV_Show_mid_COVID_df,
                 palette = 'Reds_d')
top_TV_Show_mid_COVID_graph.set_title('Top 15 TV Shows Mid-Covid', fontsize = 20)
top_TV_Show_mid_COVID_graph.set_ylabel('TV Shows', fontsize = 14)
top_TV_Show_mid_COVID_graph.set_xlabel('Duration', fontsize = 14)
top_TV_Show_mid_COVID_graph.set_xticklabels(top_TV_Show_mid_COVID_graph.get_xticklabels(), rotation = 90)


#Save the graph
top_TV_Show_mid_COVID_graph.figure.savefig('top_TV_Show_mid_COVID_graph.png')

# =============================================================================
# COVID MOVIES LIST (for Karina)
# =============================================================================

Covid_movie_views = Covid_Movie.groupby(['Title_name']
        )['Duration'].sum().sort_values(ascending = False)

Covid_top_movie = Covid_movie_views.head(15)


print(Covid_top_movie)


#Creating a dataframe for Movie
Covid_top_move_df = pd.DataFrame(Covid_top_movie)
Covid_top_move_df.reset_index(inplace = True)
Covid_top_move_df.rename(columns = {'index':'Title_name', 'Duration':'Duration'}, inplace = True)
Covid_top_move_df

#Creating a graph for Movie
plt.figure(figsize = (12, 8))
Covid_top_move_mid_COVID_graph = sns.barplot(y = "Title_name", x = "Duration", data = Covid_top_move_df,
                 palette = 'Reds_d')
Covid_top_move_mid_COVID_graph.set_title('Top Movie Mid-Covid ',   fontsize = 20)
Covid_top_move_mid_COVID_graph.set_ylabel('Movie',  fontsize = 14)
Covid_top_move_mid_COVID_graph.set_xlabel('Duration',  fontsize = 14)
Covid_top_move_mid_COVID_graph.set_xticklabels(Covid_top_move_mid_COVID_graph.get_xticklabels(), rotation = 90)

#Save the graph
Covid_top_move_mid_COVID_graph.figure.savefig('Covid_top_move_mid_COVID_graph.png')

# =============================================================================
# Save the Dataset in a new CSV as new columns were created
# =============================================================================
Karina.to_csv('Karina.csv')


