

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import time
import random


def sleep_random_time(min_t = 0, max_t = 10):
	t = random.randint(min_t, max_t);
	print "sleep %d seconds" %(t);	
	time.sleep(t);
	print "sleep ends";

def fetch_questions_from_page_num(base_url, page_num = 1):
	print "Getting questions from page: %d" % (page_num);
	current_url = base_url + "?page=" + str(page_num);
	print current_url;

	try:
		http_response = urllib2.urlopen(current_url);
		content = http_response.read();
	except Exception, e:
		tmp = "Cannot open the %d page";
		print tmp % (page_num);
		return;

	soup = BeautifulSoup(content)
	questions = soup.find_all(class_="title")
	allQuestions = [];
	for question in questions:
		try:
			allQuestions.append(question.text.decode());
		except Exception, e:
			pass;

	for question in allQuestions:
		File.write(question+"\n");



File = None;
MAX_PAGE_NUM = 337;
PAGE_NUM_TO_SLEEP = 10;
if __name__ == '__main__':
	base_url = "http://www.answerbag.com/category/transportation_506";
	File = open("answerbag-com-transportation.txt", "a");
	for page_num in range(1, 1+MAX_PAGE_NUM):
		fetch_questions_from_page_num(base_url, page_num);
		if page_num % PAGE_NUM_TO_SLEEP == 0:
			sleep_random_time(1, 5);
	File.close();



