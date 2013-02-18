from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from displaygenome.models import Genome_Stats, Replicon_Stats, Names, Nodes, Jobs, Tax_Stats
import datetime
import re
import string


def on_request(request):
    t = loader.get_template('admin/index.html')
    c = Context({
    })
    return HttpResponse(t.render(c))
    

def show_jobs(request):
    failed_jobs = Jobs.objects.filter(step_status__exact = 'Failure').order_by("-job_start_time")[:10]
    successful_jobs = Jobs.objects.filter(step_status__exact = 'Success').order_by("-job_start_time")[:10]
    t = loader.get_template('admin/index.html')
    c = Context({
        'failed_jobs': failed_jobs,
        'successful_jobs': successful_jobs,
    })
    return HttpResponse(t.render(c))
