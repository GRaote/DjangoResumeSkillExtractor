from django.conf.urls import patterns, url

from skillsdb import views


urlpatterns = patterns('',
   
	url(r'^upload/$', views.upload ,name ='file_upload'),
	url(r'^search_by_skills/$', views.search_by_skills ,name ='search_skill'),
	 url(r'^downloadfile/$', views.downloadfile ,name ='downloadfile'),
    )
