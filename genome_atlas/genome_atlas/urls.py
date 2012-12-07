from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'displaygenome.views.tax_index'),
    url(r'^genome/$', 'displaygenome.views.index'),
    url(r'^genome/(?P<genome_id>\d+)/$', 'displaygenome.views.detail'),
    url(r'^phyla/(?P<phylum_id>\d+)/$', 'displaygenome.views.phylum'),
    url(r'^phyla/children_of/(?P<parent_id>\d+)/$', 'displaygenome.views.parent_phylum'),
    url(r'^accession/(?P<accession>\w+)/$', 'displaygenome.views.accession'),
    url(r'^latest/$', 'displaygenome.views.latest'),
    url(r'^search/(?P<term>\w+)/$', 'displaygenome.views.search'),
    url(r'^search/$', 'displaygenome.views.search'),
    url(r'^admin/$', 'displaygenome.views.admin'),
    url(r'^tax/$', 'displaygenome.views.tax_index'),
    url(r'^tax/(?P<tax_id>\d+)/$', 'displaygenome.views.tax'),
    #url(r'^phyla/children_of/(?P<parent_id>\d+)/$', 'displaygenome.views.parent_phylum'),
    # Examples:
    # url(r'^$', 'genome_atlas.views.home', name='home'),
    # url(r'^genome_atlas/', include('genome_atlas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
