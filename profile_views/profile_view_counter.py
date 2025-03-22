import requests
import plotly.express as px
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
import os

# Fetch the current view count from the URL
url = "https://komarev.com/ghpvc/?username=ewkt"
response = requests.get(url)
soup = BeautifulSoup(response.content, "xml")

# Extract the view count
texts = soup.find_all("text")
view_count = int(texts[-1].text.strip())

# Get today's date in a format comprehensible for plotly
today = datetime.now().strftime("%d/%m/%y")

# File to store the view counts
file_path = "profile_views/data/view_counts.csv"

yesterday_view_count = 0
new_views = 0

if os.path.exists(file_path):
    # Read the last entry from the file to get yesterday's view count
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
        if rows:
            last_row = rows[-1]
            yesterday_view_count = int(last_row[1])

new_views = view_count - yesterday_view_count

# Append today's values to the file
with open(file_path, "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([today, view_count, new_views])

# Read the data from the file for plotting
dates = []
daily_views = []

with open(file_path, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        dates.append(row[0])
        daily_views.append(int(row[2]))

# Plot the data using plotly
fig = px.line(x=dates, y=daily_views, labels={'x': 'Date', 'y': 'Views'}, title='Daily GitHub Profile Views')
fig.update_traces(line=dict(color='blue'))
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title='Date',
        showgrid=False,
        tickformat='%d/%m/%y'
    ),
    yaxis=dict(
        title='Views',
        showgrid=False
    ),
    title=dict(
        x=0.5
    )
)
fig.write_image("profile_views/data/views_light.png")

fig.update_traces(line=dict(color='orange'))
fig.update_layout(
    plot_bgcolor='#0d1117',
    paper_bgcolor='#0d1117',
    font_color='white',
    xaxis=dict(
        title='Date',
        showgrid=False,
        tickformat='%d/%m/%y',
        color='white'
    ),
    yaxis=dict(
        title='Views',
        showgrid=False,
        color='white'
    ),
    title=dict(
        x=0.5,
        font=dict(color='white')
    )
)
fig.write_image("profile_views/data/views_dark.png")
