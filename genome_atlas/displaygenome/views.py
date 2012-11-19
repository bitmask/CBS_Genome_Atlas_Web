# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from displaygenome.models import Genome_Stats

def index(request):
    latest_genome_list = Genome_Stats.objects.all().order_by("-genome_id")[:10]

    t = loader.get_template('genomes/index.html')
    c = Context({
        'latest_genome_list': latest_genome_list,
    })
    return HttpResponse(t.render(c))

def detail(request, genome_id):
    return HttpResponse("You're looking at genome %s." % genome_id)

def frontpage(request):
    return index(request)
