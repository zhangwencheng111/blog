from django.conf.urls import url
from blog import views


urlpatterns = [
	#\w匹配包括下划线的任何单词字符。等价于'[A-Za-z0-9_]'
	url(r'^$', views.post_list, name='post_list'),
	url(r'^(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
	#url(r'^$', views.PostListView.as_view(), name='post_list'),
	url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
		r'(?P<post>[-\w]+)',
		views.post_detail,
		name='post_detail'),
	url(r'^(?P<post_id>\d+)/$', views.post_share, name="post_share")
]