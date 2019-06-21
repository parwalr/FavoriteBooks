from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'add_book$', views.add_book),
    url(r'^addtofave/(?P<id>\d+)$', views.add_fav),
    url(r'^addtofaves/(?P<id>\d+)$', views.add_favs),
    url(r'^unfavorite/(?P<id>\d+)$', views.unfave),
    url(r'^books/(?P<id>\d+)$', views.show_book),
    url(r'^books/(?P<id>\d+)/update$', views.update_info),
    url(r'^books/(?P<id>\d+)/destroy$', views.destroy),
    url(r'^users/(?P<id>\d+)$', views.user),
    url(r'^logout$', views.logout),
]