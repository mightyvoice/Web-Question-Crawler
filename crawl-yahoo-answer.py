
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import re
import time
import random

from myLibs import *
			

entry_url = "https://answers.yahoo.com/dir/index?sid=396545593";

base_url = "https://answers.yahoo.com";

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36";

http_header = {'Connection': 'Keep-Alive', 'User-Agent': user_agent};

fileName = "yahoo-answer-travel.txt";
File = open(fileName, "a");
allQuestions = [];
allQuestionUrlMD5 = [];
MAX_NUM_QUESTION = 100000;

def fetchQuestionsUrlsFromEntry():
	try:
		http_request = urllib2.Request(entry_url, None, http_header);
		http_response = urllib2.urlopen(http_request);
		content = http_response.read();
	except Exception, e:
		print "Cannot open the page of category: ";
		return;

	soup = BeautifulSoup(content)
	divs = soup.find_all(class_="Fz-14 Fw-b Clr-b Wow-bw title");
	ans = [];
	for div in divs:
		ans.append(base_url+div["href"]);
		allQuestions.append(div.text);
		File.write(div.text.encode("utf-8")+"\n");

	for url in ans:
		allQuestionUrlMD5.append(getMd5ValueOfString(url));
	return ans;

def bfsToGetAllQuestions():
	urlQueue = fetchQuestionsUrlsFromEntry();
	for question in allQuestions:
		print question;
	while len(urlQueue) > 0 and len(allQuestionUrlMD5) < MAX_NUM_QUESTION and len(allQuestions) < MAX_NUM_QUESTION:
		url = urlQueue.pop(0);
		urlMD5 = getMd5ValueOfString(url);
		try:
			# print url;
			print len(urlQueue), len(allQuestionUrlMD5), len(allQuestions);
			# http_request = urllib2.request(url, none, http_header);
			http_response = urllib2.urlopen(url);
			content = http_response.read();
		except Exception, e:
			print "cannot open current url";
			continue;

		soup = BeautifulSoup(content);
		divs = soup.find_all(class_="qstn-title Fz-13 Fw-b Wow-bw");
		for div in divs:
			tmpURL = base_url + div.a["href"];
			tmpMD5 = getMd5ValueOfString(tmpURL);
			if allQuestionUrlMD5.count(tmpMD5) == 0:
				urlQueue.append(base_url+div.a["href"]);
				allQuestions.append(div.a.text);
				allQuestionUrlMD5.append(tmpMD5);
				File.write(div.a.text.encode("utf-8")+"\n");
				# print div.a.text;
				# print div.a["href"];

	File.close();

def experimentCralwer(url):
	try:
		http_request = urllib2.Request(url, None, http_header);
		http_response = urllib2.urlopen(http_request);
		content = http_response.read();
	except Exception, e:
		print "Cannot open the page of category: ";
		return;

	soup = BeautifulSoup(content)
	divs = soup.find_all(class_="qstn-title Fz-13 Fw-b Wow-bw");
	for div in divs:
		print base_url+div.a["href"];
		print div.a.text;

if __name__ == '__main__':
	bfsToGetAllQuestions();



