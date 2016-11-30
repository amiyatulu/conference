from django.conf.urls import patterns, url
from conference import views
urlpatterns = patterns('',
                       url(r'^home/$',views.conferencehome, name="home"),
                       url(r'^sponsors/$',views.sponsors, name="sponsors"),
                       url(r'^advisory/$',views.advisory, name="advisory"),
                       url(r'^speakers/$',views.speakers, name="speakers"),
                       url(r'^registration/$',views.registrationclosed, name="registration"),
                       url(r'^registrationsuccessful/$',views.registrationsuccessful, name="registrationsuccessful"),
                       url(r'^contact/$',views.contact, name="contact"),
                       url(r'^registrationdetails/$', views.registrationdetails, name="registrationdetails" ),
                       url(r'^travel/$',views.travel, name="travel"),
                       url(r'^schedule/$',views.schedule, name="schedule"),
                       url(r'^download/$', views.download_csv, name="download"),
                       url(r'^download2/$', views.download_csv_received, name="download"),
                       url(r'^pca/(?P<chrid>\d+)/$',views.plotpcashift, name = "pca"),
                       url(r'^pca2/(?P<chrid>\d+)/$',views.plotpcashift2, name = "pca2"),
                       url(r'^pca3/(?P<chrid>\d+)/$', views.plotpcashift2color, name = "pca3"),
                       url(r'^pca4/(?P<chrid>\D+)/$', views.plotpcashift2color2, name = "pca4"),
                       )