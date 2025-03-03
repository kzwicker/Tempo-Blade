import os
os.system("pip install bs4")
from bs4 import BeautifulSoup
html_content = """
<html>
<body>
  <h1>Title</h1>
  <p>Paragraph 1</p>
  <p>Paragraph 2</p>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
</body>
</html>
"""
soup = BeautifulSoup(html_content, 'html.parser')
paragraphs = soup.find_all('p')
for p in paragraphs:
    print(p.text)