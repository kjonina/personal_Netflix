# personal_Netflix
After downloading Netflix data from my account, I decided to analyse it with pandas and practise pivoting tables.

Data was based on Family Netflix Account
Inspired by [python tutorial analyze personal netflix data](https://www.dataquest.io/blog/python-tutorial-analyze-personal-netflix-data/).

## Disclaimer
In my defence of my nightly viewing habits: I use Netflix to watch as I fall asleep. I call it my cheap cure to insomnia.
Majority of the time, I would turn on Netflix before bed and just fall asleep. 
Unfortunately, Netflix does not ask "Click to Continue" and on numerous occassions I woke up at 3am to find that Netflix kept rolling.

In March of 2012, I found myself unemployed due to COVID, so I had a lot of free time
Sometimes, when I watch movies, I code. I put something in the background, more like white noise, which does not require much thinking or attention from actual work. 
This dataset was analysed during Season 2 of iZombie!

### Variables
['Profile Name', 'Start Time', 'Duration', 'Attributes', 'Title',
'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark',
'Country']

The following Variables were removed from the data ['Device Type', 'Bookmark', 'Latest Bookmark', 'Country']
The data contains Hooks and Trailers, which were elimiated from the data as wel. These were identified as HOOK and TRAILER in ['Supplemental Video Type']. Only 'NaN' was included in the dataset.

['Start Time'] was changed to date and time using *to_datetime*
['Duration']  was changed to duration using *to_timedelta*

Another varialbe was created Type which had 2 levels: TV Show and Movie

### Users
My family watches Netflix as well, but I think I should only write about myself in this report. 

Upon initial examination, here is the table of Duration.
- Karina     90 days 01:52:53

### Examining Weekdays
What day of the week do I watch the most Netflix?

![Duration_Weekdays](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Duration_Weekdays.png)

### Examining Hour of the Day

In my defence, I use Netflix to watch as I fall asleep. I call it my cheap cure to insomnia.
Majority of the time, I would turn on Netflix before bed and just fall asleep. 
Unfortunately, Netflix does not ask "Click to Continue" and on numerous occassions I woke up at 3am to find that Netflix kept rolling.

![Duration_Hours](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Duration_Hours.png)

### Examining  Type
Type Table
-    Movie  8 days 00:12:30
-   TV Show 82 days 01:40:23

Due to enormous amount of data when viewing Top 15 so the data was split by User and then Type.

![Duration_Type](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Duration_Type.png)

### Examining Top 15 Movies 

![Duration_Movie](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Duration_Movie.png)


### Examining Top 15 TV Shows

![Duration_TV_SHow](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Duration_TV_SHow.png)

# Examining By Pre-COVID and COVID
Covid has changed my life dramatically. As I was employed in Private Education, I found myself unemployed and, apparently, a lot of free time.  
So I decided to find out how much of that viewing was made during Covid and Pre-Covid. 
Considering I am unemployed (but in a part-time course in DBS, which takes up majority of my time now, I still have a lot of viewing time while I code.


### New Variables
I created ['Normality'] which is stated by 12th of March 2020. Everything before this date is considered 'Pre-Covid', everything after is considered 'Covid'

I also split the 'Karina' dataset by 'Covid_Movies' and 'Covid_TV_Show'

### Comparing Habit Pre-Covid and Covid

![Compare_Weekdays](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Compare_Weekdays.png)

Although, weekdays seem not to have a significant changed, Covid viewing habits are nearly a third of Pre-Covid data..


![Compare_Hours](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Compare_Hours.png)

Hour has a significant difference in habits. It is clear that there is a lot more viewing during the day.


### Examining Top 15 TV Shows in Covid

![Covid_Duration_TV_SHow](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Covid_Duration_TV_SHow.png)

That is accurate, I had a 'HIMYM' marathon...

### Examining Top 15 Movie in Covid

![Covid_Duration_Movie](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Covid_Duration_Movie.png)

My movie choices are rather shameful! However, I think I was trying to beat someone in this [Netflix tweet](https://twitter.com/netflix/status/940051734650503168?ref_src=twsrc%5Etfw).

# Learning Outcomes
There is a several reasons why I did this project:
- familiarity with panda
- use to_timedate and to_timedelta
- converting datetime to date
- splitting month and year from dataset
- creatively filtering 'Title' to eliminate Seasons and Episodes and to create new variable ['Type']
- creatively filtering and splitting data (['Profile_Name',  'Type', 'Normality']
- creating pivot tables with timedelta
- faster graphs

I have started and NOT FINISHED so many datasets. I have made it my mission to finish one project. 
Although, projects are never finished. 

### To Do:
- Create a lineplot with Month+Year