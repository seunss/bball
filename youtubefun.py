import os
import datetime
import requests
import os
from pytube import YouTube



url = "https://www.youtube.com/watch?v=x2sjEj8TClM&t" # sample url
yt = YouTube(url)

print("Video views:", yt.views)
print("Video title:", yt.title)
print("Video thumbnail url:", yt.thumbnail_url)