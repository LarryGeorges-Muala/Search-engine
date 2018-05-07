from django.conf.urls import url 
from . import views

app_name = 'encyclopedia'

urlpatterns=[

	url(r'^$', views.index, name='index'),
	url(r'^search$', views.search, name='search'),
	url(r'^search/$', views.search, name='search'),
	url(r'^search/(?P<research_item>\w+)/$', views.search, name='search'),
	url(r'^ajax/researcher/$', views.researcher, name='researcher'),
	
]