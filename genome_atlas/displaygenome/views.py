# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from displaygenome.models import Genome_Stats, Replicon_Stats

def index(request):
    latest_genome_list = Genome_Stats.objects.all().order_by("-genome_id")[:10]

    accession = []
    for genome in latest_genome_list:
        accession.append(Replicon_Stats.objects.filter(genome_id__exact = genome.genome_id))
    template_array = zip(latest_genome_list, accession)

    t = loader.get_template('genomes/index.html')
    c = Context({
        'latest_genome_list': template_array
    })
    return HttpResponse(t.render(c))

def detail(request, genome_id):
    #return HttpResponse("this is id " + str(genome_id));

    genome = Genome_Stats.objects.filter(genome_id__exact = genome_id)
    replicons = Replicon_Stats.objects.filter(genome_id__exact = genome_id)
    t = loader.get_template('genomes/single.html')
    c = Context({
        'genome': genome,
        'replicons': replicons,
    })
    return HttpResponse(t.render(c))

def frontpage(request):
    return index(request)
