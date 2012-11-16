from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^genome/$', 'displaygenome.views.index'),
    url(r'^genome/(?P<genome_id>\d+)$', 'displaygenome.views.detail'),
    # Examples:
    # url(r'^$', 'genome_atlas.views.home', name='home'),
    # url(r'^genome_atlas/', include('genome_atlas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)