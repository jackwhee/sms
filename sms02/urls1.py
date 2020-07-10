"""my_sms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.conf.urls import url, include
from users import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^v1/getOpenid/$',views.index,name='index'),
    # url(r'^v1/getOpenid/(?P<webopenid>[\da-zA-Z!@#$%^&+*\-_]*)$',views.index,name='bangding'),

    # 添加users模块url映射
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^(?P<path>MP_verify_k7wWmtjzCFXUk82c.txt)$', serve, {'document_root': settings.BASE_DIR}),

    url(r'^v1/users', include('users.urls')),
    url(r'^v1/assistant$', views.assistant, name='assistant'),
    url(r'^v1/assistant_login$', views.assistant_login, name='assistant_login'),
    # url(r'^v1/assistant_register$', views.assistant_register, name='assistant_register'),
    url(r'^v1/assistant_index$', views.assistant_index, name='index'),
    url(r'^v1/assistant_search$', views.assistant_search, name='search'),
    url(r'^v1/assistant_msg$', views.assistant_msg, name='stu_msg'),
    url(r'^v1/assistant_new$', views.assistant_new, name='new_stu'),
    url(r'^v1/assistant_false$', views.assistant_false, name='false_stu'),
    url(r'^v1/assistant_distribution$', views.assistant_distribution, name='distribution'),
    url(r'^v1/assistant_sch$', views.assistant_school, name='school'),
    url(r'^v1/assistant_sch_msg$', views.assistant_sch_msg, name='school'),
    url(r'^v1/(?P<id>[\da-zA-Z!@#$%^&+*\-]*)/LOP_img$', views.LOP_img, name='LOP_img'),
    url(r'^v1/(?P<id>[\da-zA-Z!@#$%^&+*\-]*)/GPA_img$', views.GPA_imgs, name='GPA_img'),
    url(r'^v1/web_reg$', views.web_index, name='web_reg'),
    url(r'^v1/web_reg/(?P<webopenid>[\da-zA-Z!@#$%^&+*\-_]*)$', views.web_index, name='web_reg'),
    url(r'^v1/web_reg/(?P<webopenid>[\da-zA-Z!@#$%^&+*\-_]*)/web_voucher$', views.web_user_voucher, name='web_user_voucher'),
    url(r'^v1/web_reg/(?P<webopenid>[\da-zA-Z!@#$%^&+*\-_]*)/web_card_img$', views.web_card_img, name='web_card_img'),
    url(r'^v1/web_reg/(?P<webopenid>[\da-zA-Z!@#$%^&+*\-_]*)/web_GPA_img$', views.web_GPA_img, name='web_GPA_img'),
    url(r'^v1/cw_login$', views.cw_login, name='cw_login'),
    url(r'^v1/cw_index$', views.cw_index, name='cw_index'),

    url(r'^v1/cw_search$', views.cw_search, name='cw_search'),
    url(r'^v1/cw_ds$', views.cw_ds, name='cw_ds'),

    url(r'^v1/cw_new$', views.cw_new, name='cw_new'),
    url(r'^v1/cw_nds$', views.cw_nds, name='cw_nds'),
    url(r'^v1/cw_refunds$', views.cw_refunds, name='cw_refunds'),

    url(r'^v1/cw_new_msg/(?P<stu_id>[\da-zA-Z!@#$%^&+*\-_]*)$', views.cw_new_msg, name='cw_new_msg'),
    url(r'^v1/cw_stu_msg/(?P<stu_id>[\da-zA-Z!@#$%^&+*\-_]*)$', views.cw_stu_msg, name='cw_stu_msg'),
    url(r'^v1/cw_ds_msg/(?P<stu_id>[\da-zA-Z!@#$%^&+*\-_]*)$', views.cw_ds_msg, name='cw_ds_msg'),
    url(r'^v1/cw_new_ds/(?P<stu_id>[\da-zA-Z!@#$%^&+*\-_]*)$', views.cw_new_ds, name='cw_new_ds'),
    url(r'^v1/cw_ref_msg/(?P<stu_id>[\da-zA-Z!@#$%^&+*\-_]*)$', views.cw_ref_msg, name='cw_ref_msg'),

    url(r'^v1/map_test$', views.map_test, name='map_test'),

]
