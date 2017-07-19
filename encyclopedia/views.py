import wikipedia
import wolframalpha
from django.shortcuts import render

# Create your views here.

def index(request):

	message = "Search Engine"
		
	context={
		'message': message,
	}

	return render(request, 'encyclopedia/index.html', context)
	

def search(request):

	search_result = ''
	message = ''
	value_searched_on_engine = ''
	
	if request.method == 'POST':
		content_searched = request.POST.get('contentSearch', None)
		value_searched_on_engine = content_searched	
		content_searched = content_searched.lower()
		
		try:
			#WolfRamAlpha database search
			
			app_id = "G639QJ-GRP8YT7V92"

			client = wolframalpha.Client(app_id)

			res = client.query(content_searched)

			answer = next(res.results).text
			
			search_result = answer
			
			print('Value found on WolfRamAlpha')
			
		
		except:
			try:
				#Wikipedia database search
				
				answer = wikipedia.summary(content_searched)
				
				search_result = answer
				
				print('Value found on Wikipedia')
			
			except:
				search_result = 'Value Not Found... Please try another search'
				
				print('Value Not Found')
				
	
	message = "Search Engine Results"
	
	context={
		'message': message,
		'value_searched_on_engine': value_searched_on_engine,
		'search_result': search_result,
	}

	return render(request, 'encyclopedia/search.html', context)