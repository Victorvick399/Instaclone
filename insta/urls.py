from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns=[
  url(r'^$',views.home,name='Home'),
  url(r'^about',views.about,name='About'),
  url(r'^accounts/profile/',views.profile,name='Profile'),
  url(r'^new/post$', views.new_post, name='new_post'),
  url(r'^comments/<int:id>$',views.comment,name='comment'),
  url(r'^update/profile$',views.update_profile,name='update_profile'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)