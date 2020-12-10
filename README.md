# personal_Netflix
After downloading Netflix data from my account, I decided to analyse it with pandas and practise pivoting tables.

Data was based on Family Netflix Account.
Inspired by [python tutorial analyze personal netflix data](https://www.dataquest.io/blog/python-tutorial-analyze-personal-netflix-data/).

## Disclaimer
In my defence of my nightly viewing habits: I use Netflix to watch as I fall asleep. I call it my cheap cure to insomnia.
Majority of the time, I would turn on Netflix before bed and just fall asleep. 
Unfortunately, Netflix does not ask "Click to Continue" and on numerous occassions I woke up at 3am to find that Netflix kept rolling.

In March of 2020, I found myself unemployed due to COVID, so I had a lot of free time.
Sometimes, when I watch movies, I code. I put something on in the background, more like white noise, which does not require much thinking or attention from actual work. 
This dataset was analysed during Season 2 of iZombie!

# Learning Outcomes
I have started and NOT FINISHED so many datasets. I made it my mission to finish one project and write my analysis in the README.md file!
It is a goofy little project but there are a several reasons why I did this project.
I aimed and succeeed to:
- [x] build my familiarity with pandas
- [x] use to_timedate and to_timedelta
- [x] convert datetime to date
- [x] split month and year from date
- [x] creatively filter 'Title' to eliminate Seasons and Episodes and to create new variable ['Type']
- [x] split 'Title' to eliminate Seasons and Episodes and to create new variable ['Title'] to have just 'Gossip Girl' instead of 'Gossip Girl: Season 3: Episode 7'
- [x] filter and split data ['Profile_Name',  'Type', 'Normality']
- [x] create pivot tables with timedelta
- [x] practise creating graphs in pandas and seaborn
- [x] use Github and update the README.md

### Variables
['Profile Name', 'Start Time', 'Duration', 'Attributes', 'Title',
'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark',
'Country']

The following Variables were removed from the data ['Device Type', 'Bookmark', 'Latest Bookmark', 'Country'].
The data contains Hooks and Trailers, which were elimiated from the data as wel. Rows with HOOK and TRAILER in ['Supplemental Video Type'] were deleted. 
Only 'NaN' was included in the dataset.

['Start Time'] was changed to date and time using *to_datetime*.
['Duration']  was changed to duration using *to_timedelta*.

Another variable ['Type'] was created which had 2 levels: TV Show and Movie.

### Users
My family watches Netflix as well, but I think I should only write about myself in this report. 

Upon initial examination, I spent **90 days 01:52:53** watching Netflix!!

### Examining Viewing by Month and Year

**When did I watch Netflix most?**

![Karina_Month_Year_df_graph](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Karina_Month_Year_df_graph.png)

Surprised with this graph. How did I watch so much Netflix in the first few months of getting the account?
And how have I not bet it while in Covid?

### Examining Weekdays
**What day of the week do I watch the most Netflix?**

![views_per_day_df_graph](https://github.com/kjonina/personal_Netflix/blob/main/Graph/views_per_day_df_graph.png)

### Examining Hour of the Day

In my defence, I use Netflix to watch as I fall asleep. I call it my cheap cure to insomnia.
Majority of the time, I would turn on Netflix before bed and just fall asleep. 
Unfortunately, Netflix does not ask "Click to Continue" and on numerous occassions I woke up at 3am to find that Netflix kept rolling.

**What time of the day do I watch Netflix the most?**

![views_per_hour_df_graph](https://github.com/kjonina/personal_Netflix/blob/main/Graph/views_per_hour_df_graph.png)

### Examining  Type
Type Table
-    Movie  8 days 00:12:30
-   TV Show 82 days 01:40:23

Due to enormous amount of data when viewing Top 15 so the data was split by User and then Type.

**What is my preference? Movies or TV Shows?**

![views_by_Type_df_graph](https://github.com/kjonina/personal_Netflix/blob/main/Graph/views_by_Type_df_graph.png)

### Examining Top 15 Movies 

**What are my TOP 15 Movies?**

![movie_graph](https://github.com/kjonina/personal_Netflix/blob/main/Graph/movie_graph.png)

In my defence of my poor Movie choices: again, some of them, I feel asleep to, so hence, I tried to go back and find out what happens in the end. 
I am surprised that there are not more movies on the list that I watched twice... 

### Examining Top 15 TV Shows

**What are my TOP 15 TV Shows?**

![TV_Show_graph](https://github.com/kjonina/personal_Netflix/blob/main/Graph/TV_Show_graph.png)

# Examining By Pre-COVID and COVID
Covid has changed my life dramatically. As I was employed in Private Education, I found myself unemployed and, apparently, with a lot of free time.  
So I decided to find out how much of that viewing was made during Covid and Pre-Covid. 
Considering I am unemployed (but in a part-time course in DBS, which takes up majority of my time now, I still have a lot of viewing time while I code.
**I had passed both my summer exams with flying colours. Two As to be exactly**
Apparently, instead of being "Work Hard. Play Hard.", I am "Work Hard. Watch Netflix Harder." 

### New Variables
I created ['Normality'] which is stated by 12th of March 2020 
(The day that Taoiseach Leo Varadkar closed all schools, colleges and universities (both private and public) in the Republic of Ireland).
Everything before this date is considered 'Pre-Covid', everything after is considered 'Covid'.

I also split the 'Karina' dataset by 'Covid_Movies' and 'Covid_TV_Show'.

### Comparing Habit Pre-Covid and Covid

**Spot the difference: Pre-Covid and Covid**

![Compare_Weekdays](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Compare_Weekdays.png)

Although, weekdays seem not to have a significant changed, Covid viewing habits are nearly a third of Pre-Covid data.

**Spot the difference: Pre-Covid and Covid**

![Compare_Hours](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Compare_Hours.png)

Hour has a significant difference in habits. It is clear that there is a lot more viewing during the day.

### Examining Top 15 TV Shows in Covid

**What are my TOP 15 TV Shows in Covid?**

![top_TV_Show_mid_COVID_graph](https://github.com/kjonina/personal_Netflix/blob/main/Graph/top_TV_Show_mid_COVID_graph.png)

That is accurate, I had a 'HIMYM' marathon...

### Examining Top 15 Movie in Covid

**What are my TOP 15 Movie in Covid?**

![Covid_top_move_mid_COVID_graph](https://github.com/kjonina/personal_Netflix/blob/main/Graph/Covid_Duration_Movie.png)

My movie choices are rather shameful! However, I think I was trying to beat someone in this [Netflix tweet](https://twitter.com/netflix/status/940051734650503168?ref_src=twsrc%5Etfw).