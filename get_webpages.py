from bs4 import BeautifulSoup                                                  
import requests
from itertools import chain, izip
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv 

#url_pat = 'http://www.flipkart.com/mi-4i/p/itme8cuyyqdwek9m?pid=MOBE6H8AZ6PF4BVY&ref=L%#3A1746539865983692&srno=b_1&al=PjgfER0mT8GNmJSMJ1y0qsldugMWZuE7Qdj0IGOOVqvLwwmsMU1bw2bzEsGCk7xLtamqGW4kpkw%3D'

#url = 'http://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&filterNone=true'

#url from where u want to extract items
url = 'http://www.flipkart.com/mobiles/pr?p[]=facets.brand%255B%255D%3DMicromax&p[]=facets.type%255B%255D%3DSmartphones&p[]=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&p[]=sort%3Dpopularity&sid=tyy%2C4io&filterNone=true'

pid = []
item = []
dictionary = {}

def mine(URL):
	#r = requests.get(URL)
	driver = webdriver.Firefox()
	driver.get(url)
	
	driver.maximize_window();

	
	prior = 0
	while True:
    		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    		current = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "show-more-results")))
    		#print len(current.text)
    		if len(current.text) != 0:
        		break
    		prior = len(current.text)
    	
    	#element = driver.find_element_by_id("show-more-results")
    	#driver.execute_script("return arguments[0].scrollIntoView();", element)

    	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"show-more-results")))
	
	#while True:
	#	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	#	try:
	#		elem = driver.find_element_by_id("show-more-results")
	#		driver.execute_script("return arguments[0].scrollIntoView();", elem)
	#		ActionChains(driver).move_to_element(driver.find_element(By.ID, 'show-more-results'))\
  	#		.click(driver.find_element(By.ID, "show more results"))\
  	#		.perform()
  	#	except:
  	#		print "stuck"
  	#		continue
  	#	break
  	
  	elem = driver.find_element_by_id("show-more-results")
  	driver.execute_script("return arguments[0].scrollIntoView();", elem)
  	while not(driver.find_element_by_id("no-more-results").is_displayed()):
  		elem = driver.find_element_by_id("show-more-results")
  		driver.execute_script("return arguments[0].scrollIntoView();", elem)
  		if(driver.find_element_by_id("show-more-results").is_displayed()):
			ActionChains(driver).move_to_element(elem)\
  			.click(elem)\
  			.perform()
  			print "here"
  		else:
  			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  			try:
  				WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,"show-more-results")));
  			except: 
  				elem = driver.find_element_by_id("no-more-results")	
  				driver.execute_script("return arguments[0].scrollIntoView();", elem)
				


	soup = BeautifulSoup(driver.page_source)
	items = soup.find_all('div',{'id':'products'})
	for products in items:
		try:
			mobiles = products.find_all('a',{'class':"fk-display-block"})
			#print mobiles
		except:
			continue
		for phone in mobiles:
			if(phone['title']!=None):
				#print phone['title']
				index = phone['title'].index('(')
				title = phone['title'][:index]
				item.append(title)
				pid.append(phone['href'])
				dictionary[title] = phone['href']
	print item
	#print pid

#end of function 

mine(url)
w = csv.writer(open("output.csv", "w"))
for key, val in dictionary.items():
    w.writerow([key, val])
