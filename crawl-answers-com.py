
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import time
import random
			

def get_all_category_urls(entry_url):
	response = urllib2.urlopen(entry_url);
	soup = BeautifulSoup(response.read());
	ans = {};
	contents = soup.find_all(class_="category_name");
	for category in contents:
		ans[category.a.text] = category.a["href"];
	return ans;

def get_last_page_num(soup):
	div = soup.find_all(class_="last_page")
	for x in div:
		if x != None:
			return int(x.text);
	return 0;

def sleep_random_time(min_t = 0, max_t = 10):
	t = random.randint(min_t, max_t);
	print "sleep %d seconds" %(t);	
	time.sleep(t);
	print "sleep ends";

pages_num_to_sleep = 30;

def fetch_questions_from_category(base_url, categaryName = ""):

	print "Getting questions from category: " + categaryName;

	starting_page_num = 1;
	TOTAL_PAGE = 0;

	current_url = base_url + "-" + str(starting_page_num);
	try:
		http_response = urllib2.urlopen(current_url);
		content = http_response.read();
	except Exception, e:
		print "Cannot open the page of category: " + categaryName;
		return;

	soup = BeautifulSoup(content)
	TOTAL_PAGE = get_last_page_num(soup);

	#get all the question on each page
	curFile = open(categaryName+"_questions.txt", "a")
	print TOTAL_PAGE, " pages in " + categaryName;
	page_nums = range(1, TOTAL_PAGE+1);
	# random.shuffle(page_nums);
	finishedPageNum = 0;

	for cur_page_num in page_nums:

		current_url = base_url + "-" + str(cur_page_num)

		try:
			http_response = urllib2.urlopen(current_url);
			content = http_response.read();
		except Exception, e:
			tmp = "Cannot open the %d page of category: " + categaryName;
			print tmp % (cur_page_num);
			continue;

		soup = BeautifulSoup(content)
		questions = soup.find_all(class_="question")
		allQuestions = [];
		for question in questions:
			try:
				allQuestions.append(question.a.text.decode());
			except Exception, e:
				pass;

		tmp = "Finish the %d page of " + categaryName;
		print tmp % (cur_page_num);

		finishedPageNum += 1;
		if finishedPageNum >= pages_num_to_sleep:
			finishedPageNum = 0;
			sleep_random_time(0, 5);

		#write questions from current page to the file
		for question in allQuestions:
			curFile.write(question+"\n");

	curFile.close();

# finished_categories = ["Relationships", "Entertainment and Arts",
# "Law and Legal Issues", "Science",
# "Religion and Spirituality", "Shopping", "Humor and Amusement",
# "Sports", "Literature and Language", "Home and Garden", 
# "Hobbies and Collectibles", "Travel and Places",
# "History, Politics and Society", "Jobs and Education",
# "Technology", "Health", "Business and Finance", "Food and Cooking",
# "Animal Life", "Cars and Vehicles"
# ];

finished_categories = [];

def fetch_from_all_categories(entry_url):
	allCategoryUrls = get_all_category_urls(entry_url);
	for name in allCategoryUrls.keys():
		if not name in finished_categories:
			finished_categories.append(name);
			fetch_questions_from_category(allCategoryUrls[name], categaryName = name);
			print "Finish getting questions from the category: " + name;

if __name__ == '__main__':
	entry_url = "http://www.answers.com/Q/FAQ";
	fetch_from_all_categories(entry_url);
	# fetch_questions_from_category("http://www.answers.com/Q/FAQ/4116-", categaryName="travel");

