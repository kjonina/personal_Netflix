# personal_Netflix
After downloading Netflix data from my account, I decided to analyse it with pandas and practise pivoting tables.

Data was based on Family Netflix Account
Inspired by:        https://www.dataquest.io/blog/python-tutorial-analyze-personal-netflix-data/

# Variables
['Profile Name', 'Start Time', 'Duration', 'Attributes', 'Title',
'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark',
'Country']

The following Variables were removed from the data ['Device Type', 'Bookmark', 'Latest Bookmark', 'Country']
The data contains Hooks and Trailers, which were elimiated from the data as wel. These were identified as HOOK and TRAILER in ['Supplemental Video Type']. Only 'NaN' was included in the dataset.

['Start Time'] was changed to date and time using *to_datetime*
['Duration']  was changed to duration using *to_timedelta*


Upon initial examination, here is the table of Duration.
Karina     90 days 01:52:53
Karolina   21 days 17:37:15
Vit         4 days 06:26:10

