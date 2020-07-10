from django.conf.urls import url
from . import views
from sms02 import test


urlpatterns = [
    url(r'^/drop', views.drop),
    url(r'^/test$', views.test),
    # url(r'^/media/(?P<path>.*)', serve, {"document_root":settings.MEDIA_ROOT}),
    url(r'^/(?P<openid>[\da-zA-Z!@#$%^&+*\-_]*)$', views.users, name='user'),
    url(r'^/(?P<openid>[\da-zA-Z!@#$%^&+*\-_]*)/ds_registered$', views.ds_registered, name='ds_registered'),
    url(r'^/(?P<openid>[\da-zA-Z!@#$%^&+*\-_]*)/voucher$', views.user_voucher, name='user_voucher'),
    url(r'^/(?P<openid>[\da-zA-Z!@#$%^&+*\-_]*)/card_img$', views.card_img, name='card_img'),
    url(r'^/(?P<openid>[\da-zA-Z!@#$%^&+*\-_]*)/GPA_img$', views.GPA_img, name='GPA_img'),


    # url(r'^/assistant$', views.assistant, name='assistant'),
    # url(r'^/(?P<openid>[\w]{1,28})/(?P<id>[\w]{1,8})$',views.users,name='lower'),


]
