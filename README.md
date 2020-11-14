# personal_Netflix
After downloading Netflix data from my account, I decided to analyse it with pandas and practise pivoting tables.

Data was based on Family Netflix Account
Inspired by https://www.dataquest.io/blog/python-tutorial-analyze-personal-netflix-data/

# Variables
['Profile Name', 'Start Time', 'Duration', 'Attributes', 'Title',
'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark',
'Country']

The following Variables were removed from the data ['Device Type', 'Bookmark', 'Latest Bookmark', 'Country']
The data contains Hooks and Trailers, which were elimiated from the data as wel. These were identified as HOOK and TRAILER in ['Supplemental Video Type']. Only 'NaN' was included in the dataset.

['Start Time'] was changed to date and time using *to_datetime*
['Duration']  was changed to duration using *to_timedelta*

Another varialbe was created Type which had 2 levels: TV Show and Movie

# Users
My family watches Netflix as well, but I think I should only write about myself in this report. 

Upon initial examination, here is the table of Duration.
- Karina     90 days 01:52:53

# Examining Weekdays
What day of the week do I watch the most Netflix?
-   weekdays         Duration
-       Mon 11 days 06:16:13
-       Tue 11 days 01:22:45
-       Wed 12 days 06:48:28
-       Thu 13 days 02:25:43
-       Fri 14 days 08:24:55
-       Sat 15 days 13:01:07
-       Sun 12 days 11:33:42


# Examining Hour of the Day

In my defence, I use Netflix to watch as I fall asleep. I call it my cheap cure to insomnia.
Majority of the time, I would turn on Netflix before bed and just fall asleep. 
Unfortunately, Netflix does not ask "Click to Continue" and on numerous occassions I woke up at 3am to find that Netflix kept rolling.


# Examining  Type
-                  Movie          TV Show                                        
- Karina   8 days 00:12:30 82 days 01:40:23

Due to enormous amount of data when viewing Top 15 so the data was split by User and then Type.

# Examining Top 15 Movies 
- Gone Girl                     09:40:01 - fantastic movie
- Gattaca                       06:08:54 - "You want to know how I did it? This is how I did it, Anton: I never saved anything for the swim back."
- Pride & Prejudice             05:05:23 
- Divergent                     04:39:50 - 
- Wedding Crashers              04:34:33 - A classic!
- Inglourious Basterds          04:23:21 
- The Maze Runner               04:16:24 - 
- New Year's Eve                04:11:43 - Again, tried to watch it at least three times and I fell asleep each time. 
- Marriage Story                04:10:32 - Fantastic movie about a marriage breaking down
- P.S. I Love You               04:03:57 - Watched it at least twice with in my English Language class
- He's Just Not That Into You   04:01:22
- The Break-Up                  03:58:16 
- Baywatch                      03:35:24 
- The Hangover                  03:19:22 
- Leap Year                     03:12:29 - Watched it at least twice with in my English Language class

# Examining Top 15 TV Shows
- Gossip Girl                   7 days 10:16:19
- How I Met Your Mother         6 days 16:40:53
- Brooklyn Nine-Nine            6 days 07:05:39
- The Vampire Diaries           5 days 12:58:14
- How to Get Away With Murder   5 days 10:12:54
- Marvel's Jessica Jones        3 days 16:49:54
- Dynasty                       3 days 10:45:15
- iZombie                       2 days 22:24:23
- Money Heist                   2 days 22:14:52
- Sons of Anarchy               2 days 14:22:31
- Suits                         2 days 11:17:31
- House of Cards                2 days 00:56:52
- Riverdale                     1 days 22:06:32
- You                           1 days 20:28:53
- Spartacus                     1 days 17:06:22

In my defence of my Top 15: Sometimes, when I watch movies, I code. I put something in the background, more like white noise, which does not require much thinking or attention from actual work. 

# Examining By Pre-COVID and COVID
Covid has changed my life dramatically. As I was employed in Private Education, I found myself unemployed and, apparently, a lot of free time.  
So I decided to find out how much of that viewing was made during Covid and Pre-Covid. 
Considering I am unemployed (but in a part-time course in DBS, which takes up majority of my time now), I still have a lot of viewing time while I code.


# New Variables
I created ['Normality'] which is stated by 12th of March 2020. Everything before this date is considered 'Pre-Covid', everything after is considered 'Covid'

I also split the 'Karina' dataset by 'Covid_Movies' and 'Covid_TV_Show'

# Comparing Habit Pre-Covid and Covid
Weekdays have not seen a significant changed

Hour has a significant different habits. It is clear that there is a lot more viewing during the day.


# Examining Top 15 TV Shows in Covid


# Examining Top 15 Movie in Covid