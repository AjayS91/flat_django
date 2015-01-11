from django.conf.urls import patterns, include, url
from accounts.views import register,save_details,loginview,updateview,deleteview,logoutview,index
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls),name='admin'),
    url(r'^register/', register, name='register'),
    url(r'^save/',save_details,name='save'),
    url(r'login/',loginview,name='login'),
    url(r'^update/',updateview,name='update'),
    url(r'^logout/',logoutview,name='logout'),
    url(r'^delete/',deleteview,name='delete'),
    url(r'^$',index,name='index')
)
