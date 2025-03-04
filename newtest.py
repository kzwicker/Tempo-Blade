from bs4 import BeautifulSoup
import requests
import os
def get_website_source(url):
  """
  Retrieves the source code of a website.

  Args:
    url: The URL of the website.

  Returns:
    The source code of the website as a string, or None if an error occurs.
  """
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"Error fetching URL '{url}': {e}")
    return None

page_source = get_website_source("https://beatsaver.com/?q=starships").encode("utf-8")
if page_source is None:
   quit()
   """
search = "starships"
text = requests.get(f"http://beatsaver.com/?q={search}").text
soup = BeautifulSoup(text, "html.parser")
hello = soup.find_all("body")
for x in hello:
   print(x.text)
print(hello)
"""
filename = "website.html"
folder = "Songs/"
goofy = os.name == "nt"
open(filename, 'wb').write(page_source)