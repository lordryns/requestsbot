import requests
from bs4 import BeautifulSoup

request = requests.get("https://bothaven.netlify.app")

soup = BeautifulSoup(request.content, "html.parser")

for tag in soup.find_all("div"):
  print(tag)