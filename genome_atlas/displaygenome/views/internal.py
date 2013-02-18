from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from displaygenome.models import Genome_Stats, Replicon_Stats, Names, Nodes, Jobs, Tax_Stats
import datetime
import re
import string

"""
This file is a view request file.

This view is responsible for explaining how to access the database directly.

"""

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def on_request(request):

    client_ip = get_client_ip(request) 
    if client_ip.startswith("10.57."):
        t = loader.get_template('internal.html')
        c = Context({
        })  
        return HttpResponse(t.render(c))
    else:
        return HttpResponseRedirect("/")
    
