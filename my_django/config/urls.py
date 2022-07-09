"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.urls import include
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from apiv1 import views
from . import settings

urlpatterns = [
  path('admin/',    admin.site.urls),
  path('api/v1/',   include('apiv1.urls')),

  path('',          RedirectView.as_view(url='/admin/'), name='index'),  # FW: http://〜:8080/    => http://〜:8080/admin
  path('api/',      RedirectView.as_view(url='/api/v1/'), name='apiv1'), # FW: http://〜:8080/api => http://〜:8080/api/v1/
  path('api-auth/', include('rest_framework.urls')),  # !! DRF のログイン機能を使う(akiyoko rest2: P110)
]

#--------------------------------------------------------------------------------
# CoreAPI を使うための設定
#--------------------------------------------------------------------------------
if ('coreapi' in settings.MY_DEBUG) and (settings.MY_DEBUG['coreapi'] is True): # !!
  from django.conf import settings
  from rest_framework.documentation import include_docs_urls
  title = "SiTrace RESTful APIドキュメント"
  detail = ""
  urlpatterns += [
    #path('docs/', include_docs_urls(title='APIドキュメント')), # http://localhost:8000/docs
    path('docs/', include_docs_urls(title=title, description=detail)), # http://localhost:8000/docs
  ]

#--------------------------------------------------------------------------------
# SQL パネルを使うための設定
#--------------------------------------------------------------------------------
if ('toolbar' in settings.MY_DEBUG) and (settings.MY_DEBUG['toolbar'] is True): # !!
  import debug_toolbar
  urlpatterns += [
    path('^__debug__/', include(debug_toolbar.urls)),
  ]

