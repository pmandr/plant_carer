from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^attach/', views.attach, name='attach'),
    url(r'^send_update/', views.send_update, name='send_update'),
    url(r'^test/', views.test, name='test'),
]
