import wikipedia
import wolframalpha
import traceback
import requests
import json
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
try:
	from django.urls import reverse
except:
	from django.core.urlresolvers import reverse
from encyclopedia import keys, emailer

def record_visit():
	pass

def index(request):
	record_visit()
	return render(request, 'encyclopedia/index.html', context={})


def send_error_email(error):
	try:
		error_log = '''
		**************************************
		Search Engine Error
		-------------------

		{}
		__
		{}

		**************************************
		'''.format(str(error), str(traceback.format_exc()))
		send_mail(
			subject='Search Engine Log',
			message=error_log,
			from_email='Search Engine',
			recipient_list= emailer.SERVER_NOTIFIER,
			fail_silently=True
		)
	except Exception as e:
		print()
		print('Error Log:', error)
		print()
		print('Email Log:', e)
		print()

'''
	Custom Searches
'''
def filter_search_result(x):
	if x:
		x = x.replace('"', '`')
		x = ''.join(x.splitlines())
	return x

def make_soup(x):
	r = requests.get(x)
	soup = BeautifulSoup(r.text, "html.parser")
	return soup

def generate_wolfram_result(research_item):
	search_result_wolfram = ''
	try:
		#WolfRamAlpha database search
		client = wolframalpha.Client(keys.wolframalpha_key)
		res = client.query(research_item)
		search_result_wolfram = next(res.results).text
		search_result_wolfram = filter_search_result(search_result_wolfram)
		print('Value found on WolfRamAlpha')
	except Exception as error:
		send_error_email(error)
		print('Value Not Found on WolfRamAlpha')
	return search_result_wolfram

def generate_wikipedia_result(research_item):
	search_result_wiki = ''
	try:
		#Wikipedia database search
		search_result_wiki = wikipedia.summary(research_item)
		search_result_wiki = filter_search_result(search_result_wiki)
		print('Value found on Wikipedia')
	except Exception as error:
		send_error_email(error)
		print('Value Not Found on Wikipedia')
	return str(search_result_wiki)

def generate_youtube_result(research_item):
	search_result_youtube = ''
	try:
		#Youtube search
		youtube_url_to_scrape = 'https://www.youtube.com/results?search_query=' + research_item
		soup = make_soup(youtube_url_to_scrape)
		for link in soup.findAll('a', {'class': 'yt-uix-tile-link'}):
			video_ID = link['href'].split('/watch?v=')
			if len(video_ID[-1]) < 12:
				search_result_youtube = video_ID[-1]
				break
		print('Value Found on Youtube')
	except Exception as error:
		send_error_email(error)
		print('Value Not Found on Youtube')
	return search_result_youtube

def generate_collins_result(research_item):
	search_result_collins = ''
	try:
		#Collins search
		collins_url_to_scrape = 'https://www.collinsdictionary.com/dictionary/english/' + research_item
		soup = make_soup(collins_url_to_scrape)
		for link in soup.findAll('div', {'class': 'content definitions cobuild br'}):
			search_result_collins += link.text
		search_result_collins = filter_search_result(search_result_collins)
		print('Value Found on Collins')
	except Exception as error:
		send_error_email(error)
		print('Value Not Found on Collins')
	return search_result_collins

def generate_webster_result(research_item):
	search_result_webster = ''
	try:
		#webster search
		webster_url_to_scrape = 'https://www.merriam-webster.com/dictionary/' + research_item
		soup = make_soup(webster_url_to_scrape)
		for link in soup.findAll('div', {'class': 'vg'}):
			search_result_webster += link.text
		search_result_webster = filter_search_result(search_result_webster)
		print('Value Found on webster')
	except Exception as error:
		send_error_email(error)
		print('Value Not Found on webster')
	return search_result_webster

def generate_oxford_result(research_item):
	search_result_oxford = ''
	try:
		#Oxford search
		oxford_url_to_scrape = 'https://en.oxforddictionaries.com/definition/' + research_item
		soup = make_soup(oxford_url_to_scrape)
		for link in soup.findAll('ul', {'class': 'semb'}):
			search_result_oxford += link.text
			break
		search_result_oxford = filter_search_result(search_result_oxford)
		print('Value Found on Oxford')
	except Exception as error:
		send_error_email(error)
		print('Value Not Found on Oxford')
	return search_result_oxford
'''
	End Custom Searches
'''


def test_stuff(search_result_wolfram, search_result_wiki, search_result_youtube, search_result_collins, search_result_webster, search_result_oxford):
	test_mode = False
	if test_mode:
		search_result_wolfram = 'Result from Wolf'
		search_result_wiki = 'Result from Wiki'
		search_result_youtube = 'ABCDEFGH'
		search_result_collins = 'Result from Collins'
		search_result_webster = 'Result from webster'
		search_result_oxford = 'Result from Oxford'
		huge_text = 'Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32. The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.'
		search_result_wolfram = huge_text
		search_result_wiki = huge_text
		search_result_collins = huge_text
		search_result_webster = huge_text
		search_result_oxford = huge_text
	return search_result_wolfram, search_result_wiki, search_result_youtube, search_result_collins, search_result_webster, search_result_oxford


def search(request, research_item=''):
	''' Django Request '''
	search_result_wolfram = ''
	search_result_wiki = ''
	search_result_youtube = ''
	search_result_collins = ''
	search_result_webster = ''
	search_result_oxford = ''

	if not research_item:
		research_item = request.GET.get('contentSearch', None)

	if research_item:
		search_result_wolfram = generate_wolfram_result(research_item.lower())
		search_result_wiki = generate_wikipedia_result(research_item.lower())
		search_result_youtube = generate_youtube_result(research_item.lower())
		search_result_collins = generate_collins_result(research_item.lower())
		search_result_webster = generate_webster_result(research_item.lower())
		search_result_oxford = generate_oxford_result(research_item.lower())

	search_result_wolfram, search_result_wiki, search_result_youtube, search_result_collins, search_result_webster, search_result_oxford = test_stuff(search_result_wolfram, search_result_wiki, search_result_youtube, search_result_collins, search_result_webster, search_result_oxford)

	context={
		'research_item': research_item,
		'search_result_wolfram': search_result_wolfram,
		'search_result_wiki': search_result_wiki,
		'search_result_youtube': search_result_youtube,
		'search_result_collins': search_result_collins,
		'search_result_webster': search_result_webster,
		'search_result_oxford': search_result_oxford
	}
	return render(request, 'encyclopedia/search.html', context)


def researcher(request):
	''' WIP - Ajax Request '''
	research_item = request.GET.get('researcher', None)
	search_result_wolfram = ''
	search_result_wiki = ''
	search_result_youtube = ''
	search_result_collins = ''
	search_result_oxford = ''

	if research_item:
		search_result_wolfram = generate_wolfram_result(research_item.lower())
		search_result_wiki = generate_wikipedia_result(research_item.lower())
		search_result_youtube = generate_youtube_result(research_item.lower())
		search_result_collins = generate_collins_result(research_item.lower())
		search_result_webster = generate_webster_result(research_item.lower())
		search_result_oxford = generate_oxford_result(research_item.lower())

	search_result_wolfram, search_result_wiki, search_result_youtube, search_result_collins, search_result_webster, search_result_oxford = test_stuff(search_result_wolfram, search_result_wiki, search_result_youtube, search_result_collins, search_result_webster, search_result_oxford)

	data = {
		'is_taken': True,
		'searched_for': research_item,
		'search_result_wolfram': search_result_wolfram,
		'search_result_wiki': search_result_wiki,
		'search_result_youtube': search_result_youtube,
		'search_result_collins': search_result_collins,
		'search_result_webster': search_result_webster,
		'search_result_oxford': search_result_oxford
	}
	#return JsonResponse(json.dumps(data))
	return JsonResponse(data)
