import requests
import plotly.express as px
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
import os

#fetch the current view count from the URL
url = "https://komarev.com/ghpvc/?username=ewkt"
response = requests.get(url)
soup = BeautifulSoup(response.content, "xml")

#extract the view count
texts = soup.find_all("text")
view_count = int(texts[-1].text.strip())

#get today's date in a format comprehensible for plotly
today = datetime.now().strftime("%Y-%m-%d")

#file to store the view counts
file_path = "view_counts.csv"

yesterday_view_count = 0
new_views = 0

if os.path.exists(file_path):
    #read the last entry from the file to get yesterday's view count
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
        if rows:
            last_row = rows[-1]
            yesterday_view_count = int(last_row[1])

new_views = view_count - yesterday_view_count

#append today's values to the file
with open(file_path, "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([today, view_count, new_views])

#read the data from the file for plotting
dates = []
daily_views = []

with open(file_path, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        dates.append(row[0])
        daily_views.append(int(row[2]))

#plot the data using plotly
fig = px.line(x=dates, y=daily_views, labels={'x': 'Date', 'y': 'Views'}, title='GitHub Profile Views (Daily)')
fig.update_layout(xaxis_title='Date', yaxis_title='Views')
fig.write_image("views.png")
