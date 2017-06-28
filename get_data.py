import dill
import re
from bs4 import BeautifulSoup
import requests
'''
Get random #

Open that URL

Wait for it to redirect

Get that data

Save TITLE, RATING, INGREDIENTS,ID

'''

def get_redirect(url):
	url_trunk='http://allrecipes.com/recipe/'+str(url)
	print url_trunk
	page=requests.get(url_trunk)
	print unicode(page.text)
	#soup=BeautifulSoup(page.text,'lxml')
	return 

def call_number():

	return


url_id=24908
print get_redirect(url_id)
