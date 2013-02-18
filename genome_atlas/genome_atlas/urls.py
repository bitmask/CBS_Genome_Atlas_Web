from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Index Page
    url(r'^$', 'displaygenome.views.index.on_request'),    
    
    # Score Page 
    url(r'^score/$', 'displaygenome.views.score.on_request'),

    # Internal direct to db access info page
    url(r'^internal/$', 'displaygenome.views.internal.on_request'),
    
    url(r'^search/$', 'displaygenome.views.search.on_request'),
    url(r'^search/w+/$','displaygenome.views.search.on_request'),

    # /browse -> displaygenome.views.browse.request
    # url(r'^tax/(?P<tax_id>\d+)/$', 'displaygenome.views.tax'),
    url(r'^browse/$', 'displaygenome.views.index.on_request'),
    url(r'^browse/1/$', 'displaygenome.views.index.on_request'),
    url(r'^browse/(?P<tax_id>\d+)/$', 'displaygenome.views.browse.on_request'),

    # /admin -> worry about this later
    url(r'^jobs/$', 'displaygenome.views.admin.on_request'),

    url(r'^download/$', 'displaygenome.views.download.on_request'),
    url(r'^download/genomes$', 'displaygenome.views.download.genomes'),
    url(r'^download/replicons$', 'displaygenome.views.download.replicons'),

    #    url(r'^genome/$', 'displaygenome.views.index'),
    #url(r'^genome/(?P<genome_id>\d+)/$', 'displaygenome.views.detail'),
    #url(r'^phyla/(?P<phylum_id>\d+)/$', 'displaygenome.views.phylum'),
    #url(r'^phyla/children_of/(?P<parent_id>\d+)/$', 'displaygenome.views.parent_phylum'),
    #url(r'^accession/(?P<accession>\w+)/$', 'displaygenome.views.accession'),
    #url(r'^latest/$', 'displaygenome.views.latest'),
    #url(r'^search/(?P<term>\w+)/$', 'displaygenome.views.search'),
    #url(r'^search/$', 'displaygenome.views.search'),
    #url(r'^tax/$', 'displaygenome.views.tax_index'),

    #url(r'^phyla/children_of/(?P<parent_id>\d+)/$', 'displaygenome.views.parent_phylum'),
    # Examples:
    # url(r'^$', 'genome_atlas.views.home', name='home'),
    # url(r'^genome_atlas/', include('genome_atlas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
