from django.conf.urls.defaults import patterns, include, url

from tastypie.api import Api
from eg.api.resources import (
                                ListFieldTestResource,
                                DictFieldTestResource,
                                EmbeddedModelFieldTestResource,
                                EmbeddedListFieldTestResource,
                               )


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

v1_api = Api(api_name='v1')

v1_api.register(ListFieldTestResource())
v1_api.register(DictFieldTestResource())
v1_api.register(EmbeddedModelFieldTestResource())
v1_api.register(EmbeddedListFieldTestResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'src.views.home', name='home'),
    # url(r'^src/', include('src.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),

)
