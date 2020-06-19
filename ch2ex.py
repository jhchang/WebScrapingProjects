from urllib.request import urlopen 
from bs4 import BeautifulSoup
import re
    
html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html, 'html.parser')

images = bs.find_all(lambda tag: len(tag.attrs) == 2)

for img in images:
	print(img)
	print("=========================================================")
