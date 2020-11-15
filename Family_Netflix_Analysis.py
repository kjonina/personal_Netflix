

"""
Name:               Karina Jonina 
Github:             https://github.com/kjonina/
Data Gathered:      based on Family Netflix Account
Inspired by:        https://www.dataquest.io/blog/python-tutorial-analyze-personal-netflix-data/
"""
# =============================================================================
# Droping Columns
# =============================================================================
df = df.drop(['Attributes', 'Bookmark', 'Latest Bookmark', 'Country', 'Device Type'], axis = 1)

print(df.head())

#creating a new variable called SVT where data is null or not null
df['SVT'] = df['Supplemental Video Type'].isnull()

# Trying to create  a dataset with only True as SVT
df = df[df.SVT == True]

#dropping unnecesary columns
df = df.drop(['SVT', 'Supplemental Video Type'], axis = 1)


# =============================================================================
# Correcting Variables Types
# =============================================================================
#checking data types
df.dtypes

#changing Profile Name to a categorical variable
df['Profile Name'] = df['Profile Name'].astype('category')

# changing Start Time to Date Time in UTC Time Zone
df['Start Time'] = pd.to_datetime(df['Start Time'], utc = True)

#changing Duration to time account
df['Duration'] = pd.to_timedelta(df['Duration'])


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
# Analysing by Time
# =============================================================================

df['Start Time'].unique()

df['Date'] = df['Start Time'].dt.date

df['year'] = pd.DatetimeIndex(df['Date']).year
df['month'] = pd.DatetimeIndex(df['Date']).month

# =============================================================================
# Creating a Variable examining Pre-Covid and Covid
# =============================================================================
#Pre-Covid is before 12th March 2020 (That is the day that I was last in work)
df.loc[df['Date'] < datetime.date(2020,3,12), 'normality'] = 'Pre-Covid'
df.loc[df['Date'] > datetime.date(2020,3,12), 'normality'] = 'Covid'

df['normality'] = df['normality'].astype('category')

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
# Creating separate datasets for Each User
# =============================================================================

Karina = df[df['Profile Name'] == 'Karina']

#Profile Name
#Karina     90 days 01:52:53
#Karolina   21 days 17:37:15
#Vit         4 days 06:26:10


''' FIx graph '''
# Examines the Profile Names 
plt.figure(figsize = (12, 8))
sns.countplot(x = 'Profile Name', data = df, palette = 'viridis', order = df['Profile Name'].value_counts().index)
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


# create the table
df.groupby('Profile Name')['weekdays'].value_counts()

# create  the table
views_per_day = df.groupby(
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

df['hour'] = df['Start Time'].dt.hour

df['hour'] = pd.Categorical(df['hour'], 
       categories = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
       ordered = True)

# create the table
views_per_Vit = df.groupby(
        ['Profile Name', 'hour']
        )['Duration'].count().reset_index()


plotdata1 = views_per_Vit.pivot(index = 'Profile Name',
                                columns = 'hour',
                                values = 'Duration')

plotdata1.plot(kind = 'bar')

df.groupby('Profile Name')['hour'].value_counts()

# =============================================================================
# Creating variable called Type: Tv Show or Movie
# =============================================================================

#trying to create the all the names with Season and create  a new variable called Type
df.loc[df['Title'].str.contains(': '), 'Type'] = 'TV Show'

#Trying to create  Movie in Type
df.loc[df['Type'].isnull(), 'Type'] = 'Movie'


#visualising duration and profile Name type
views_per_Vit_by_Type = df.groupby(
        ['Profile Name', 'Type']
        )['Duration'].sum().reset_index()

#Creating table to view Duration by Name and Type
pivot_movie_name = pd.DataFrame({'A': df['Profile Name'],
                   'B': df['Type'],
                   'C': df['Duration']})

# Pivoting the talbe
pivot_movie_name = pd.pivot_table(pivot_movie_name, values='C', index=['A'], columns=['B'], aggfunc='sum')

#Produce the table
print(pivot_movie_name)
#B                   Movie          TV Show
#A                                         
#Karina   22 days 03:48:58 67 days 22:03:55
#Karolina 10 days 04:41:23 11 days 12:55:52
#Vit       1 days 10:28:40  2 days 19:57:30

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

df['Title_name'] = (np.where(df['Title'].str.contains(': '),
                  df['Title'].str.split(':').str[0],
                  df['Title']))


views_by_Title_name = df.groupby(['Title_name']
        )['Duration'].sum().reset_index()


# =============================================================================
# Duration by Profile Name and Titles
# =============================================================================
#visualising duration by profile Name and title
views_by_Title_name = df.groupby(
        ['Title_name']
        )['Duration'].sum().sort_values(ascending=False)

#Creating table to view Duration by Name and title
pivot_title_name = pd.DataFrame({'A': df['Profile Name'],
                   'B': df['Title_name'],
                   'C': df['Duration']})

# Pivoting the table
pivot_title_name1 = pd.pivot_table(pivot_title_name, values='C', index=['B'], columns=['A'], aggfunc='sum')

#Produce the table
print(pivot_title_name1)


# =============================================================================
# Creating separate datasets for each Vit to analyse Top Movies and TV Shows for each Vit
# =============================================================================

Karina = df[df['Profile Name'] == 'Karina']

Karolina = df[df['Profile Name'] == 'Karolina']

Vit = df[df['Profile Name'] == 'Vit']


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
# Examining dataset by Vit
# =============================================================================

#Creating the view of Vit's viewing habits
views_by_Vit = Vit.groupby(
        ['Title_name', 'Type']
        )['Duration'].sum().sort_values(ascending=False)

# Viewing Vit's Top 50 most watched (in Duration) Tv Shows and Movies
views_by_Vit.head(50)

# Viewing Karolina's Bottom 15 watched (in Duration) Tv Shows and Movies
views_by_Vit.tail(15)

#examining the shape of the data
print(views_by_Vit.shape)


'''
FUTURE RESEARCH IDEAS

Draw line graph with time + duration with 3 different lines for each Vit

create  a snapshot of when the Vits are all using Netflix

Analyse Titles

Run an algorythm to analyse who will watch which TV SHows and Movies with what titles?
'''


