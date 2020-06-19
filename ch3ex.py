from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

#Retrieves a list of all Internal links found on a page
def getInternalLinks(bs, includeUrl):
	includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme,
		urlparse(includeUrl).netloc)
	internalLinks = []
	#Finds all links that begin with a "/"
	#or find links that have the site name in the url
	for link in bs.find_all('a',
		href=re.compile('^(/|.*'+includeUrl+')')):
		if link.attrs['href'] is not None:
			if link.attrs['href'] not in internalLinks:
				if(link.attrs['href'].startswith('/')):
					#print(link.attrs['href'] + " ~ "*7 + includeUrl)
					internalLinks.append(
                		includeUrl+link.attrs['href'])
				else:
					#print(link.attrs['href'] + " ~ "*7 + includeUrl)
					internalLinks.append(link.attrs['href'])
	#print('='*10 + '\n' + str(internalLinks) +  '\n'+ '='*10)
	return internalLinks


#Retrieves a list of all external links found on a page
def getExternalLinks(bs, excludeUrl): 
	externalLinks = []
	#Finds all links that start with "http" that do
	#not contain the current URL
	for link in bs.find_all('a',
		href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
		if link.attrs['href'] is not None:
			if link.attrs['href'] not in externalLinks:
				#print(link.attrs['href'] + " - "*7 + excludeUrl)
				externalLinks.append(link.attrs['href'])
	return externalLinks

def getRandomExternalLink(startingPage):
	html = urlopen(startingPage)
	bs = BeautifulSoup(html, 'html.parser')
	externalLinks = getExternalLinks(bs,
		urlparse(startingPage).netloc)
	if len(externalLinks) == 0:
		print('No external links, looking around the site for one')
		domain = '{}://{}'.format(urlparse(startingPage).scheme,
			urlparse(startingPage).netloc)
		internalLinks = getInternalLinks(bs, domain)
		return getRandomExternalLink(internalLinks[random.randint(0,
									len(internalLinks)-1)])
	else:
		return externalLinks[random.randint(0, len(externalLinks)-1)]


def followExternalOnly(startingSite):
	externalLink = getRandomExternalLink(startingSite)
	print('Random external link is: {}'.format(externalLink))
	followExternalOnly(externalLink)


# Collects a list of all external URLs found on the site
allExtLinks = set()
allIntLinks = set()
def getAllExternalLinks(siteUrl):
	html = urlopen(siteUrl)
	domain = '{}://{}'.format(urlparse(siteUrl).scheme,
		urlparse(siteUrl).netloc)
	bs = BeautifulSoup(html, 'html.parser')
	internalLinks = getInternalLinks(bs, domain)
	externalLinks = getExternalLinks(bs, urlparse(siteUrl).netloc)
	for link in externalLinks:
		if link not in allExtLinks:
			allExtLinks.add(link)
			print(link)
	for link in internalLinks:
		if link not in allIntLinks:
			#print()
			#print("adding internalLink: " + link)
			#print()
			allIntLinks.add(link)
			getAllExternalLinks(link)

allIntLinks.add('http://oreilly.com')
getAllExternalLinks('http://oreilly.com')

#followExternalOnly('http://oreilly.com')

















