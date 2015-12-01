
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import re
import time
import random
import threading

from myLibs import *
			

# entry_url = "http://ca.askalo.com/";
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36";
http_header = {'Connection': 'Keep-Alive', 'User-Agent': user_agent};

fileName = "askalo-com.txt";
File = open(fileName, "a");
allQuestions = [];
allQuestionUrlMD5 = [];
MAX_NUM_QUESTION = 100000;

def getRealUrl(url):
	endPoint = -1;
	for i in range(len(url)):
		if url[i] >= '0' and url[i] <= '9' and url[i+1] == "/":
			endPoint = i;
			break;
	return url[:endPoint+1];

def fetchQuestionsUrlsFromEntry(entry_url):
	try:
		# http_request = urllib2.Request(entry_url, None, http_header);
		http_response = urllib2.urlopen(entry_url);
		content = http_response.read();
	except Exception, e:
		print "Cannot open the page of category: ";
		return;

	soup = BeautifulSoup(content)
	divs = soup.find_all(class_="resultRow");
	allUrls = [];
	for div in divs:
		allUrls.append(getRealUrl(div.a["href"]));
		# allQuestions.append(div.a.text);
		File.write(div.a.text.encode("utf-8")+"\n");

	for url in allUrls:
		allQuestionUrlMD5.append(getMd5ValueOfString(url));
	# print ans;
	# print allQuestions;
	return allUrls;

def bfsToGetAllQuestions(entry_url):
	urlQueue = fetchQuestionsUrlsFromEntry(entry_url);
	for question in allQuestions:
		print question;
	countProcessed = 0;
	while len(urlQueue) > 0 and len(allQuestionUrlMD5) < MAX_NUM_QUESTION:
		url = urlQueue.pop(0);
		urlMD5 = getMd5ValueOfString(url);
		# url = "http://sanjose.askalo.com/ID_100241072"
		try:
			# print url;
			print len(urlQueue), len(allQuestionUrlMD5);
			# http_request = urllib2.request(url, none, http_header);
			print url;
			countProcessed += 1;
			if countProcessed >= 30:
				sleep_random_time(0, 5);
				countProcessed = 0;
			http_response = urllib2.urlopen(url);
			# http_response = urllib2.urlopen(http_request);
			content = http_response.read();
		except Exception, e:
			print "cannot open current url";
			continue;

		soup = BeautifulSoup(content);
		divs = soup.find_all(class_="related_ads");
		for div in divs:
			for td in div.find_all("tr"):
				tmpURL = getRealUrl(td.a["href"]);
				tmpMD5 = getMd5ValueOfString(tmpURL);
				if allQuestionUrlMD5.count(tmpMD5) == 0:
					urlQueue.append(tmpURL);
					# allQuestions.append(td.a.text);
					allQuestionUrlMD5.append(tmpMD5);
					File.write(td.a.text.encode("utf-8")+"\n");


def getAllStateAndCityUrl(entry_url):
	try:
		# http_request = urllib2.Request(url, None, http_header);
		http_response = urllib2.urlopen(entry_url);
		content = http_response.read();
	except Exception, e:
		print "Cannot open the page";
		return;

	soup = BeautifulSoup(content)
	divs = soup.find_all(class_="chp_city");
	ans = [];
	for div in divs:
		ans.append(div.a["href"]);
	return ans;

def experimentCralwer(url):
	try:
		# http_request = urllib2.Request(url, None, http_header);
		http_response = urllib2.urlopen(url);
		content = http_response.read();
	except Exception, e:
		print "Cannot open the page";
		return;

	soup = BeautifulSoup(content)
	divs = soup.find_all(class_="related_ads");
	for div in divs:
		for td in div.find_all("tr"):
			print td.a["href"];

if __name__ == '__main__':
	# bfsToGetAllQuestions();
	# experimentCralwer("http://sanfrancisco.askalo.com/ID_100102107")
	allEntryURLs = getAllStateAndCityUrl("http://www.askalo.com/");
	for entry_url in allEntryURLs:
		tmp = entry_url;
		print tmp;
		print "Processing the place: ", tmp.split(".")[0][7:];
		bfsToGetAllQuestions(entry_url);
	File.close();
	# fetchQuestionsUrlsFromEntry();

