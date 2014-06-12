from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('bugs.views',
	url(r'^$', 'landing', name='landing'),
	url(r'^dataview/$', 'dataview', name='dataview'),
	)
