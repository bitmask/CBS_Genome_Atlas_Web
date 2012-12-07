from django.template import Context, loader
from django.http import HttpResponse
from displaygenome.models import Genome_Stats, Replicon_Stats, Names, Nodes, Jobs, Tax_Stats
import datetime
import re


def tax_index(request):
    top_level_phyla = Tax_Stats.objects.extra(where=["tax_id in (28889, 28890, 651137, 57723, 201174, 200783, 67819, 976, 67814, 204428, 74201, 1090, 200795, 200938, 1117, 200930, 1298, 270, 68297, 74152, 65842, 57723, 1239, 32066, 142182, 256845, 40117, 203682, 1224, 203691, 508458, 544448, 200940, 189775, 200918, 74201)"])
    t = loader.get_template('tax/index.html')
    c = Context({
        'phyla': top_level_phyla,
    })
    return HttpResponse(t.render(c))

def tax(request, tax_id):
    tax_level = Tax_Stats.objects.filter(tax_id__exact = tax_id).exclude(accession__isnull=False)
    
    parent_ids = ""
    top = 0
    ptax_id = tax_id
    while top < 1:
        this = Nodes.objects.using('taxonomy').filter(tax_id__exact = ptax_id)
        for row in this: #only one row since tax_id is the primary key
            print "parent: " + str(row.parent_tax_id)
            if row.parent_tax_id == 1: # TODO should match list in above query
                top = 1
            if parent_ids == "":
                parent_ids = str(row.parent_tax_id)
            else:
                parent_ids = parent_ids + ", " + str(row.parent_tax_id)
            ptax_id = row.parent_tax_id

    parent_level = Tax_Stats.objects.extra(where=["tax_id in (" + parent_ids + ")"]).exclude(accession__isnull=False).order_by('genome_count').reverse()

    #get the children of the request tax_id
    children = Nodes.objects.using('taxonomy').filter(parent_tax_id__exact = tax_id)

    child_ids = ""
    for child in children:
        if child_ids == "":
            child_ids = str(child.tax_id)
        else:
            child_ids = child_ids + ", " + str(child.tax_id)
        print "child: " + str(child.tax_id)
    
    if child_ids == "":
        child_level = Tax_Stats.objects.filter(tax_id__exact = tax_id).exclude(accession__isnull=True).order_by('accession')
    else:
        child_level = Tax_Stats.objects.extra(where=["tax_id in (" + child_ids  + ")"]).exclude(accession__isnull=False).order_by('tax_name')



    t = loader.get_template('tax/index.html')
    c = Context({
        'parents': parent_level,
        'phyla': tax_level,
        'children': child_level,
    })
    return HttpResponse(t.render(c))




def latest(request):
    latest_genome_list = Genome_Stats.objects.all().order_by("-genome_id")[:10]
    #latest_genome_list = Genome_Stats.objects.filter(modify_date__gt=datetime.date(2012, 01, 10)).order_by("-genome_id") #yyyyddmm
    accession = []
    for genome in latest_genome_list:
        accession.append(Replicon_Stats.objects.filter(genome_id__exact = genome.genome_id))
    genome_list = zip(latest_genome_list, accession)
    t = loader.get_template('genomes/index.html')
    c = Context({
        'latest_genome_list': genome_list,
    })
    return HttpResponse(t.render(c))


def index(request):
    top_level_phyla = Nodes.objects.using('taxonomy').extra(where=["tax_id in (28889, 28890, 651137, 57723, 201174, 200783, 67819, 976, 67814, 204428, 74201, 1090, 200795, 200938, 1117, 200930, 1298, 270, 68297, 74152, 65842, 57723, 1239, 32066, 142182, 256845, 40117, 203682, 1224, 203691, 508458, 544448, 200940, 189775, 200918, 74201)"])
    top_level_phyla_names = Names.objects.using('taxonomy').extra(where=["tax_id in (28889, 28890, 651137, 57723, 201174, 200783, 67819, 976, 67814, 204428, 74201, 1090, 200795, 200938, 1117, 200930 , 1298, 270, 68297, 74152, 65842, 57723, 1239, 32066, 142182, 256845, 40117, 203682, 1224, 203691, 508458, 544448, 200940, 189775, 200918, 74201)"]).filter(name_class__exact = "scientific name")


    phyla = zip(top_level_phyla, top_level_phyla_names)

    parent_tax_id = "" 

    t = loader.get_template('genomes/index.html')
    c = Context({
        'phyla': phyla,
        'parent_tax_id': parent_tax_id,
    })
    return HttpResponse(t.render(c))

def phylum(request, phylum_id):
    # Display a single phyla and it's details
    t = loader.get_template('phyla/index.html')
    phyla_no = Nodes.objects.using('taxonomy').filter(tax_id__exact = phylum_id)
    phyla_na = Names.objects.using('taxonomy').filter(tax_id__exact = phylum_id)

    c = Context({
        'phyla': zip(phyla_no, phyla_na),
        'parent_id': phyla_no[0].parent_tax_id
    })
    return HttpResponse(t.render(c))

def parent_phylum(request, parent_id):
    # Display the children of the given phyla
    t = loader.get_template('phyla/index.html')
    phyla_no = Nodes.objects.using('taxonomy').filter(parent_tax_id__exact = parent_id)
    phyla_na = Names.objects.using('taxonomy').filter(name_class__exact = "scientific name").extra(where=["tax_id in (select tax_id from nodes where parent_tax_id = %s)"], params=[parent_id]).order_by("-name_txt")
    phyla = zip(phyla_no, phyla_na)


    phyla_tax_id = "";
    for p in (phyla_no):
        if len(phyla_tax_id) == 0:
            phyla_tax_id = str(p.tax_id)
        else:
            phyla_tax_id = phyla_tax_id + ", " + str(p.tax_id)
    
    genome_list = Genome_Stats.objects.extra(where=["tax_id in (" + phyla_tax_id + ")"])
    accession = []
    for genome in genome_list:
        accession.append(Replicon_Stats.objects.filter(genome_id__exact = genome.genome_id))
    phyla_genome_list = zip(genome_list, accession)

    c = Context({
        'phyla': phyla,
        'parent_id': parent_id,
        'genome_list': phyla_genome_list,
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
  
def accession(request, accession):
    genome_id = Replicon_Stats.objects.filter(accession__exact = accession)
    print "genome_id " + str(genome_id[0].genome_id)
    return detail(request, genome_id[0].genome_id)

def search(request):
    #term could be a name, accession number, tax id
    term = request.GET.get('q', '')

    thing = ""
    if re.match(r'[A-Z]{2}[0-9]+', term, re.I):
        thing = Replicon_Stats.objects.filter(accession__exact = term)
        print "accession search: " + str(thing[0].accession)
    elif re.match(r'[0-9]+', term):
        thing = Nodes.objects.using('taxonomy').filter(tax_id__exact = term)
        print "tax id search: " + str(thing[0].tax_id)
    else:
        thing = Genome_Stats.objects.filter(genome_name__contains = term)
        print "genome name search: " + str(thing[0].genome_id)

    return HttpResponse("searched for " + term)

def admin(request):
    failed_jobs = Jobs.objects.filter(step_status__exact = 'Failure').order_by("-job_start_time")[:10]
    successful_jobs = Jobs.objects.filter(step_status__exact = 'Success').order_by("-job_start_time")[:10]
    t = loader.get_template('admin/index.html')
    c = Context({
        'failed_jobs': failed_jobs,
        'successful_jobs': successful_jobs,
    })
    return HttpResponse(t.render(c))

def frontpage(request):
    return index(request)



