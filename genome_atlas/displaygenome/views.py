# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the list of all the genomes.")

def detail(request, genome_id):
    return HttpResponse("You're looking at genome %s." % genome_id)
