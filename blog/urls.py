from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<url_slug>[\w-]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives$', views.ArchivesView.as_view(), name='archives'),
#   url(r'^tagcloud\.html$', views.tagcloud, name='tag'),
    url(r'^tagcloud$', views.TagcloudView.as_view(), name='tagcloud'),
    url(r'^tag/(?P<name>[\w,-]+)$', views.TagsView.as_view(), name='tag'),
    url(r'^category/(?P<name>[\w,-]+)$', views.CategoryView.as_view(), name='category'),
    url(r'^about$', views.AboutView.as_view(), name='about'),
]
