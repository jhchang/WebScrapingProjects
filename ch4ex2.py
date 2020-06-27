import requests
from bs4 import BeautifulSoup

class Content:
	"""Common base class for all articles/pages"""
	
	def __init__(self, topic, url, title, body):
		self.topic = topic
		self.url = url
		self.title = title
		self.body = body

	def print(self): 
		"""
		Flexible printing function controls output
		"""
		print("New article found for topic: {}".format(self.topic))
		print("URL: {}".format(self.url))
		print("TITLE: {}".format(self.title))
		print("BODY:\n{}".format(self.body))

class Website:
	"""Contains information about website structure"""
	def __init__(self, name, url, searchUrl, resultListing,
		resultUrl, absoluteUrl, titleTag, bodyTag):
		self.name = name
		self.url = url
		self.searchUrl = searchUrl
		self.resultListing = resultListing
		self.resultUrl = resultUrl
		self.absoluteUrl=absoluteUrl
		self.titleTag = titleTag
		self.bodyTag = bodyTag

class Crawler:
	def getPage(self, url):
		try:
			req = requests.get(url)
		except requests.exceptions.RequestException:
			return None
		return BeautifulSoup(req.text, 'html5lib')
	
	def safeGet(self, pageObj, selector):
		selectedElems = pageObj.select(selector)
		if selectedElems is not None and len(selectedElems) > 0:
			elems = []
			for elem in selectedElems:
				elems.append(elem.get_text()) 
			return '\n'.join(elems)
		return ''

	def search(self, topic, site):
		"""
		Searches a given website for a given topic and records all pages found
		"""
		bs = self.getPage(site.searchUrl + topic)
		searchResults = bs.select(site.resultListing)
		for result in searchResults:
			url = result.select(site.resultUrl)[0].attrs["href"]
			# Check to see whether it's a relative or an absolute URL
			if(site.absoluteUrl):
				bs = self.getPage(url)
			else:
				bs = self.getPage(site.url + url)
			if bs is None:
				print("Something was wrong with that page or URL. Skipping!")
				return
			title = self.safeGet(bs, site.titleTag)
			body = self.safeGet(bs, site.bodyTag)
			#print(title + '*'*10 + body)
			if title != '' and body != '':
				content = Content(topic, url, title, body)
				content.print()
			else:
				print("ERROR: " + title)
			print('\n'+'-'*80+'\n')



crawler = Crawler()

"""
o'reilly only selects the product results from the search
"""


siteData = [
	['O\'Reilly Media', 'http://oreilly.com',
		'https://ssearch.oreilly.com/?q=','article.product-result',
		'p.title a', True, 'h1', 'div.product-description'],
	['Reuters', 'http://reuters.com',
		'http://www.reuters.com/search/news?blob=',
		'div.search-result-content','h3.search-result-title a',
		False, 'h1', 'div.StandardArticleBody_body'],
	['Brookings', 'http://www.brookings.edu',
		'https://www.brookings.edu/search/?s=',
		'div.list-content article', 'h4.title a', True, 'h1',
		'div.post-body, div.techstream--content']
]

sites = []
for row in siteData:
	sites.append(Website(row[0], row[1], row[2],
						 row[3], row[4], row[5], row[6], row[7]))

topics = ['python']
topics = ['python', 'data science']
for topic in topics:
	print("GETTING INFO ABOUT: " + topic)
	print('\n'+'='*80+'\n')
	for targetSite in sites:
		crawler.search(topic, targetSite)
		print('\n'+'~'*80+'\n')









