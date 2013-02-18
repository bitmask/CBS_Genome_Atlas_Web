from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from displaygenome.models import Genome_Stats, Replicon_Stats, Names, Nodes, Jobs, Tax_Stats
import datetime
import re
import string

"""
This file is a view request file.

This view is responsible for explaining the 'score' heuristic.

(steve @29.1.13: I don't think any complicated view functions should show up here...)
"""
def on_request(request):
    t = loader.get_template('score.html')
    c = Context({
    })  
    return HttpResponse(t.render(c))
    
