import requests
from bs4 import BeautifulSoup

year = input("What year would you like to travel to? (Type in YYYY-MM-DD format): ")
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}

response = requests.get(url = f"https://www.billboard.com/charts/hot-100/{year}/",headers=header)
# print(response.status_code) Check status of connection
content = response.text
soup = BeautifulSoup(content,"html.parser")
all_songs = soup.select("li h3.c-title") #Get the correct css selector
song_list=[]
for song in all_songs:
    song_list.append(song.text.strip())
print(f"List of top 100 songs on {year}:\n{song_list}")


